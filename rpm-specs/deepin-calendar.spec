%global repo dde-calendar
%global __provides_exclude_from ^%{_libdir}/deepin-aiassistant/.*\\.so$

Name:           deepin-calendar
Version:        5.14.8
Release:        %autorelease
Summary:        Calendar for Deepin Desktop Environment
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-calendar
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Sql)
BuildRequires:  cmake(Qt5LinguistTools)

BuildRequires:  cmake(DtkWidget)
BuildRequires:  cmake(DtkCore)
BuildRequires:  cmake(DtkGui)

BuildRequires:  pkgconfig(libical)

BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme
Recommends:     deepin-manual

%description
Calendar for Deepin Desktop Environment.

%prep
%autosetup -p1 -n %{repo}-%{version}

sed -i 's|lib/deepin-aiassistant/serivce-plugins|${CMAKE_INSTALL_LIBDIR}/deepin-aiassistant/serivce-plugins|' \
    schedule-plugin/CMakeLists.txt

%build
%cmake -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}
%cmake_build

%install
%cmake_install
install -pDm644 calendar-client/assets/dde-calendar/calendar/common/dde-calendar.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/dde-calendar.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%doc README.md
%license LICENSE
%{_bindir}/dde-calendar
%{_sysconfdir}/xdg/autostart/dde-calendar-service.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/applications/dde-calendar.desktop
%{_datadir}/icons/hicolor/scalable/apps/dde-calendar.svg
%{_libdir}/deepin-aiassistant/serivce-plugins/libuosschedulex-plugin.so
%{_datadir}/deepin-manual/
%{_userunitdir}/com.dde.calendarserver.calendar.timer
%{_userunitdir}/*.service
%{_libexecdir}/deepin-daemon/dde-calendar-service
%dir %{_datadir}/dde-calendar
%dir %{_datadir}/dde-calendar/data
%{_datadir}/dde-calendar/data/huangli.db
%{_datadir}/deepin-log-viewer/deepin-log.conf.d/org.deepin.calendar.json
%{_datadir}/metainfo/org.deepin.calendar.metainfo.xml

%changelog
%autochangelog
