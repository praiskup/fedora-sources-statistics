# header-only library
%global debug_package %{nil}

%global forgeurl https://github.com/brofield/simpleini
Version:        4.22
%forgemeta

Name:           simpleini
Release:        %autorelease
Summary:        Cross-platform C++ library to read and write INI-style configuration files
License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://github.com/brofield/simpleini/pull/74
Patch0:         0001-cmake-fix-namespace-and-include-dir-74.patch
Patch1:         0001-convert-use-libicu-by-default.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  cmake(GTest)
BuildRequires:  libicu-devel

%description
simpleini is a cross-platform library that provides a simple API to read and
write INI-style configuration files. It supports data files in ASCII, MBCS and
Unicode. It is designed explicitly to be portable to any platform and has been
tested on Windows, WinCE and Linux. Released as open-source and free using the
MIT licence.

%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Requires:       libicu-devel

%description    devel
The %{name}-devel package contains development files for %{name}.

%prep
%forgeautosetup -p1

%build
%cmake \
    -DSIMPLEINI_USE_SYSTEM_GTEST=ON

%cmake_build

%install
%cmake_install

%check
%ctest

%files devel
%license LICENCE.txt
%doc README.md
%{_includedir}/SimpleIni.h
%{_datadir}/cmake/SimpleIni/

%changelog
%autochangelog
