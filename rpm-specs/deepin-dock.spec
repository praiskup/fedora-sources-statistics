%global repo dde-dock
%global __provides_exclude_from ^%{_prefix}/lib/dde-.*\\.so$

%global start_logo start-here

Name:           deepin-dock
Version:        6.0.37
Release:        %autorelease
Summary:        The dock of Deepin Desktop Environment
License:        LGPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-dock
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules

BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5WaylandClient)
BuildRequires:  cmake(Qt5XkbCommonSupport)
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  qt5-linguist
# provides /usr/lib64/libQt5XkbCommonSupport.a
BuildRequires:  qt5-qtbase-static

BuildRequires:  cmake(DtkGui)
BuildRequires:  cmake(DtkWidget)
BuildRequires:  cmake(DtkCMake)
BuildRequires:  cmake(dbusmenu-qt5)
BuildRequires:  cmake(DWayland)

BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(dbusmenu-qt5)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(gio-2.0)

Requires:       deepin-qt-dbus-factory
Requires:       xcb-util-wm
Requires:       xcb-util-image

%description
Deepin desktop-environment - Dock module.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1 -n %{repo}-%{version}

# set icon to Fedora logo
sed -i 's|deepin-launcher|%{start_logo}|' frame/item/launcheritem.cpp

sed -i 's|lrelease|lrelease-qt5|' translate_generation.sh

%build
%cmake -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}
%cmake_build

%install
%cmake_install
%find_lang dde-dock --all-name --with-qt
rm %{buildroot}%{_datadir}/dde-dock/translations/dde-dock.qm

%files -f dde-dock.lang
%license LICENSE
%doc README.md CHANGELOG.md plugins/plugin-guide
%{_bindir}/dde-dock
%dir %{_prefix}/lib/dde-dock
%dir %{_prefix}/lib/dde-dock/plugins
%{_prefix}/lib/dde-dock/plugins/*.so
%{_prefix}/lib/dde-dock/plugins/loader/libpluginmanager.so
%{_prefix}/lib/dde-dock/plugins/quick-trays/*.so
%dir %{_datadir}/dde-dock
%{_datadir}/dde-dock/window_patterns.json
%{_datadir}/glib-2.0/schemas/com.deepin.dde.dock.module.gschema.xml
%{_datadir}/polkit-1/actions/org.deepin.dde.dock.overlay.policy
%dir %{_sysconfdir}/dde-dock
%dir %{_sysconfdir}/dde-dock/indicator
%config(noreplace) %{_sysconfdir}/dde-dock/indicator/keybord_layout.json
%{_datadir}/dsg/configs/dde-dock/*.json

%files devel
%{_includedir}/dde-dock/
%{_libdir}/pkgconfig/dde-dock.pc
%{_libdir}/cmake/DdeDock/

%changelog
%autochangelog
