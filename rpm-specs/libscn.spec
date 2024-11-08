%global intname scn
%global upname %{intname}lib

Name: libscn
Version: 3.0.1
Release: %autorelease

License: Apache-2.0
Summary: Library for replacing scanf and std::istream
URL: https://github.com/eliaskosunen/%{upname}
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://github.com/eliaskosunen/scnlib/commit/f3b00eca89ee923e4b03a950dee0d00da48e7001
Patch100: %{name}-3.0.1-benchmark-fix.patch

BuildRequires: doctest-devel
BuildRequires: fast_float-devel
# Since fast_float is header-only, we are required to BR the -static virtual
# Provide for dependency tracking purposes.
BuildRequires: fast_float-static
BuildRequires: gmock-devel
BuildRequires: google-benchmark-devel
BuildRequires: gtest-devel

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build

%description
%{upname} is a modern C++ library for replacing scanf and std::istream.

This library attempts to move us ever so closer to replacing iostreams
and C stdio altogether. It's faster than iostream (see Benchmarks) and
type-safe, unlike scanf. Think {fmt} but in the other direction.

This library is the reference implementation of the ISO C++ standards
proposal P1729 "Text Parsing".

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: fast_float-devel

%description devel
%{summary}.

%prep
%autosetup -n %{upname}-%{version} -p1

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DSCN_BENCHMARKS:BOOL=ON \
    -DSCN_DOCS:BOOL=OFF \
    -DSCN_EXAMPLES:BOOL=OFF \
    -DSCN_INSTALL:BOOL=ON \
    -DSCN_PEDANTIC:BOOL=OFF \
    -DSCN_TESTS:BOOL=ON \
    -DSCN_USE_EXTERNAL_FAST_FLOAT:BOOL=ON \
    -DSCN_USE_EXTERNAL_GTEST:BOOL=ON \
    -DSCN_USE_EXTERNAL_BENCHMARK:BOOL=ON \
    -DSCN_USE_EXTERNAL_REGEX_BACKEND:BOOL=ON \
    -DSCN_WERROR:BOOL=OFF
%cmake_build

%check
%ctest

%install
%cmake_install
rm -rf %{buildroot}%{_datadir}/%{intname}

%files
%doc README.md
%license LICENSE
%{_libdir}/%{name}.so.3*

%files devel
%{_includedir}/%{intname}/
%{_libdir}/cmake/%{intname}/
%{_libdir}/%{name}.so

%changelog
%autochangelog
