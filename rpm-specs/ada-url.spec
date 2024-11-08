Name:		ada-url
Version:	2.9.2

%global forgeurl https://github.com/%{name}/ada
%forgemeta

Release:	%autorelease
Summary:	WHATWG-compliant and fast URL parser written in modern C++

License:	Apache-2.0 OR MIT
URL:		https://www.ada-url.com/
Source0:	%forgesource

Patch0:		1000-Remove-cmake-CPM.patch

BuildRequires:	cmake
BuildRequires:	gcc-c++

BuildRequires:	cmake(fmt)
BuildRequires:	cmake(cxxopts)

BuildRequires:	cmake(GTest)
BuildRequires:	cmake(benchmark)
BuildRequires:	cmake(simdjson)

BuildRequires:	doxygen

%description
Ada is a fast and spec-compliant URL parser written in C++.
Specification for URL parser can be found from the WHATWG website.

The Ada library passes the full range of tests from the specification,
across a wide range of platforms.
It fully supports the relevant Unicode Technical Standard.

%package tools
Summary:	Tools for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains command line utility for parsing URL.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:	Developer documentation for %{name}
Recommends:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
The %{name}-doc package contains developer documentation for
the %{name} package.

%prep
%forgeautosetup -p1

%build
%cmake \
%if 0%{?fedora} <= 39
  -DBUILD_TESTING:BOOL=OFF
%endif
%cmake_build

doxygen ./doxygen

%install
%cmake_install


%check
%ctest

%files
%license LICENSE-MIT LICENSE-APACHE
%doc README.md docs/cli.md
%{_libdir}/libada.so.2*

%files tools
%{_bindir}/adaparse

%files devel
%{_libdir}/libada.so
%{_libdir}/cmake/ada/
%{_includedir}/ada/
%{_includedir}/ada.h
%{_includedir}/ada_c.h

%files doc
%doc docs/html/

%changelog
%autochangelog

