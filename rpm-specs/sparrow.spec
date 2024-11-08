Name:           sparrow
Version:        0.0.4
Release:        %autorelease
Summary:        C++20 idiomatic APIs for the Apache Arrow Columnar Format
License:        Apache-2.0
URL:            https://github.com/man-group/sparrow
%global github  https://github.com/man-group/sparrow
Source:         %{github}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  doctest-devel

Patch0:         https://github.com/man-group/sparrow/pull/199.patch

# there is no actual arched content - this is a header only library
%global debug_package %{nil}

%global _description \
sparrow is an implementation of the Apache Arrow Columnar format in C++. It \
provides array structures with idiomatic APIs and convenient conversions from \
and to the C interface.

%description %_description

%package devel
Summary:        %{summary}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel %_description

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTS=ON -DUSE_DATE_POLYFILL=OFF
%cmake_build

%install
%cmake_install

%check
%cmake_build --target test_sparrow_lib
%{__cmake_builddir}/test/test_sparrow_lib

%files devel
%doc README.md
%license LICENSE
%{_includedir}/%{name}
%{_datadir}/cmake/%{name}

%changelog
%autochangelog
