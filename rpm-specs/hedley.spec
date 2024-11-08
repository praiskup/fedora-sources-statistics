Name:           hedley
Summary:        A C/C++ header to help move #ifdefs out of your code
Version:        15
Release:        %autorelease

URL:            https://nemequ.github.io/hedley/
%global forgeurl https://github.com/nemequ/hedley
Source:         %{forgeurl}/archive/v%{version}/hedley-%{version}.tar.gz
# The CC0-1.0 license is *not allowed* in Fedora for code, but this package
# falls under the following blanket exception:
#
#   Existing uses of CC0-1.0 on code files in Fedora packages prior to
#   2022-08-01, and subsequent upstream versions of those files in those
#   packages, continue to be allowed. We encourage Fedora package maintainers
#   to ask upstreams to relicense such files.
#
# https://gitlab.com/fedora/legal/fedora-license-data/-/issues/91#note_1151947383
License:        CC0-1.0

# This is a header-only library; there is no compiled code and therefore no
# debuginfo.
%global debug_package %{nil}

BuildRequires:  gcc-c++
BuildRequires:  make

%global common_description %{expand:
Hedley is a single C/C++ header you can include in your project to enable
compiler-specific features while retaining compatibility with all compilers. It
contains dozens of macros to help make your code easier to use, harder to
misuse, safer, faster, and more portable.

You can safely include Hedley in your public API, and it works with virtually
any C or C++ compiler.}

%description %{common_description}


%package devel
Summary:        %{summary}

BuildArch:      noarch

Provides:       hedley-static = %{version}-%{release}

%description devel %{common_description}


%prep
%autosetup


# No build section required for single-header library with single-header source


%install
install -t %{buildroot}%{_includedir} -p -m 0644 -D hedley.h


%check
# As far as we can tell, the tests are intended to be used by compiling them,
# not by running the result. See .travis.yml.
%make_build -C test


%files devel
%license COPYING
%doc NEWS
%doc README.md

%{_includedir}/hedley.h


%changelog
%autochangelog
