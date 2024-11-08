Name:           re2
%global tag 2024-07-02
%global so_version 11
Version:        %(echo '%{tag}' | tr -d -)
Epoch:          1
Release:        %autorelease
Summary:        C++ fast alternative to backtracking RE engines

# The entire source is BSD-3-Clause, except:
#   - lib/git/commit-msg.hook is Apache-2.0, but is not used in the build and
#     is removed in %%prep
License:        BSD-3-Clause
URL:            https://github.com/google/re2
Source:         %{url}/archive/%{tag}/re2-%{tag}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

BuildRequires:  cmake(absl)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  cmake(GTest)
BuildRequires:  cmake(benchmark)

# Python extension
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pybind11}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_packaging_header_only_libraries
BuildRequires:  pybind11-static

# Python extension tests
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist absl-py}

%global common_description %{expand:
RE2 is a fast, safe, thread-friendly alternative to backtracking regular
expression engines like those used in PCRE, Perl, and Python. It is a C++
library.}

%description %{common_description}


%package        devel
Summary:        C++ header files and library symbolic links for re2

Requires:       re2%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel %{common_description}

This package contains the C++ header files and symbolic links to the shared
libraries for re2. If you would like to develop programs using re2, you will
need to install re2-devel.


%package -n     python3-google-re2
Summary:        RE2 Python bindings

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_requiring_base_package
Requires:       re2%{?_isa} = %{epoch}:%{version}-%{release}

Conflicts:      python3-fb-re2
Obsoletes:      python3-fb-re2 < 1.0.7-19

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-re2

%description -n python3-google-re2
A drop-in replacement for the re module.

It uses RE2 under the hood, of course, so various PCRE features (e.g.
backreferences, look-around assertions) are not supported. See
https://github.com/google/re2/wiki/Syntax for the canonical reference, but
known syntactic ”gotchas” relative to Python are:

  • PCRE supports \Z and \z; RE2 supports \z; Python supports \z,
    but calls it \Z. You must rewrite \Z to \z in pattern strings.

Known differences between this module’s API and the re module’s API:

  • The error class does not provide any error information as attributes.
  • The Options class replaces the re module’s flags with RE2’s options as
    gettable/settable properties. Please see re2.h for their documentation.
  • The pattern string and the input string do not have to be the same type.
    Any str will be encoded to UTF-8.
  • The pattern string cannot be str if the options specify Latin-1 encoding.


%prep
%autosetup -n re2-%{tag}
# Show that a file licensed Apache-2.0 is not used in the build and does not
# contribute to the licenses of the binary RPMs:
rm lib/git/commit-msg.hook


%generate_buildrequires
cd python
%pyproject_buildrequires


%build
%cmake \
    -DRE2_BUILD_TESTING:BOOL=ON \
    -DRE2_USE_ICU:BOOL=ON \
    -GNinja
%cmake_build

cat >> python/setup.cfg <<EOF
[build_ext]
include_dirs=${PWD}
library_dirs=${PWD}/%{_vpath_builddir}
EOF
cd python
%pyproject_wheel


%install
%cmake_install

cd python
%pyproject_install
%pyproject_save_files -l re2


%check
%ctest

# Run the tests from the top-level directory to make sure we don’t accidentally
# import the “un-built” package instead of the one in the buildroot.
ln -s python/re2_test.py
LD_LIBRARY_PATH='%{buildroot}%{_libdir}' %pytest re2_test.py


%files
%license LICENSE
%doc README
%{_libdir}/libre2.so.%{so_version}{,.*}


%files          devel
%doc doc/syntax.{html,txt}
%{_includedir}/re2/
%{_libdir}/libre2.so
%{_libdir}/pkgconfig/re2.pc
%{_libdir}/cmake/re2/


%files -n       python3-google-re2 -f %{pyproject_files}


%changelog
%autochangelog
