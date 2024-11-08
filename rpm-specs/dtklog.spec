Name:           dtklog
Version:        0.0.1
Release:        %autorelease
Summary:        Simple, convenient and thread safe logger for Qt-based C++ apps
License:        LGPL-2.1-or-later
URL:            https://github.com/linuxdeepin/dtklog
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake

BuildRequires:  cmake(Qt5Core)
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  cmake(spdlog)
BuildRequires:  pkgconfig(libsystemd)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1

%build
%cmake \
    -DBUILD_WITH_SYSTEMD=ON \
    -DBUILD_WITH_QT6=OFF \
    -DDLOG_VERSION=%{version} \

%cmake_build

%install
%cmake_install

%files
%license LICENSE.LGPL
%doc README.md
%{_libdir}/libdtklog.so.0*

%files devel
%{_libdir}/libdtklog.so
%{_includedir}/dtk5/DLog/
%{_libdir}/cmake/DtkLog/
%{_libdir}/pkgconfig/dtklog.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_dtklog.pri

%changelog
%autochangelog
