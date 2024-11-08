%global __provides_exclude_from ^%{_qt5_plugindir}.*\.so$

Name:           deepin-kwin
Version:        5.25.26
Release:        %autorelease
Summary:        KWin configuration for Deepin Desktop Environment
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/deepin-kwin
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  extra-cmake-modules

BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Quick)
BuildRequires:  cmake(Qt5QuickWidgets)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5UiTools)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  cmake(Qt5Test)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5XkbCommonSupport)

BuildRequires:  cmake(Qt5FontDatabaseSupport)
BuildRequires:  cmake(Qt5ThemeSupport)
BuildRequires:  cmake(Qt5ServiceSupport)
BuildRequires:  cmake(Qt5EventDispatcherSupport)

BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
# /usr/lib64/libQt5XkbCommonSupport.a
BuildRequires:  qt5-qtbase-static

BuildRequires:  cmake(KF5Auth)
BuildRequires:  cmake(KF5Config)
BuildRequires:  cmake(KF5ConfigWidgets)
BuildRequires:  cmake(KF5CoreAddons)
BuildRequires:  cmake(KF5Crash)
BuildRequires:  cmake(KF5DBusAddons)
BuildRequires:  cmake(KF5GlobalAccel)
BuildRequires:  cmake(KF5I18n)
BuildRequires:  cmake(KF5IconThemes)
BuildRequires:  cmake(KF5IdleTime)
BuildRequires:  cmake(KF5Notifications)
BuildRequires:  cmake(KF5Package)
BuildRequires:  cmake(KF5Plasma)
BuildRequires:  cmake(KF5WidgetsAddons)
BuildRequires:  cmake(KF5WindowSystem)

BuildRequires:  cmake(KF5Declarative)
BuildRequires:  cmake(KF5KCMUtils)
BuildRequires:  cmake(KF5NewStuff)
BuildRequires:  cmake(KF5Service)
BuildRequires:  cmake(KF5TextWidgets)
BuildRequires:  cmake(KF5XmlGui)
BuildRequires:  cmake(KF5ItemViews)

BuildRequires:  cmake(KF5Wayland)
BuildRequires:  cmake(KF5Activities)
BuildRequires:  cmake(KF5DocTools)
BuildRequires:  cmake(KF5Runner)
BuildRequires:  cmake(KF5Kirigami2)
BuildRequires:  cmake(KF5Completion)

BuildRequires:  kdecoration5-devel
BuildRequires:  kscreenlocker5-devel
# BuildRequires:  cmake(KDecoration2)

# not needed in the future
BuildRequires:  cmake(DWayland)
BuildRequires:  cmake(Breeze)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libxcvt)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-cursor)
BuildRequires:  pkgconfig(xcb-damage)
BuildRequires:  pkgconfig(xcb-glx)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  xcb-util-devel

BuildRequires:  freetype-devel
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  cmake(QAccessibilityClient)

BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  qt5-qtwayland-devel
BuildRequires:  wayland-devel
BuildRequires:  cmake(DeepinWaylandProtocols)

BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  libXtst-devel

BuildRequires:  kf5-kglobalaccel-devel

Requires:       deepin-qt5integration%{?_isa}

# since F31
Obsoletes:      deepin-wm <= 1.9.38
Obsoletes:      deepin-wm-switcher <= 1.1.9
Obsoletes:      deepin-metacity <= 3.22.24
Obsoletes:      deepin-metacity-devel <= 3.22.24
Obsoletes:      deepin-mutter <= 3.20.38
Obsoletes:      deepin-mutter-devel <= 3.20.38

%description
This package provides a kwin configuration that used as the new WM for Deepin
Desktop Environment.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kwin-devel%{?_isa}
Requires:       qt5-qtx11extras-devel%{?_isa}
Requires:       gsettings-qt-devel%{?_isa}
Requires:       dtkcore-devel%{?_isa}
Requires:       kf5-kglobalaccel-devel%{?_isa}

%description    devel
Header files and libraries for %{name}.

%prep
%autosetup -p1

%build
%cmake_kf5 -GNinja
%cmake_build

%install
%cmake_install

%find_lang deepin-kwin --all-name

%files -f deepin-kwin.lang
%doc README.md
%license LICENSES/*
%{_sysconfdir}/skel/.config/kglobalshortcutsrc
%{_sysconfdir}/xdg/
%{_bindir}/deepin-kwin_*
%{_datadir}/applications/org.kde.deepin-kwin_rules_dialog.desktop
%{_datadir}/config.kcfg/deepin-*.kcfg
%{_datadir}/deepin-kwin/
%{_datadir}/dsg/configs/org.deepin.kwin/org.deepin.kwin.splitmenu.display.json
%{_datadir}/icons/hicolor/*/apps/deepin-kwin.png
%{_datadir}/icons/hicolor/scalable/apps/deepin-kwin.svgz
%{_datadir}/kconf_update/
%{_datadir}/knotifications5/deepin-kwin.notifyrc
%{_datadir}/knsrcfiles/deepin-*.knsrc
%{_datadir}/knsrcfiles/deepin-window-decorations.knsrc
%{_datadir}/kpackage/kcms/deepin-kcm_kwin_effects/
%{_datadir}/kpackage/kcms/deepin-kcm_kwin_virtualdesktops/
%{_datadir}/kpackage/kcms/deepin-kcm_kwindecoration/
%{_datadir}/kpackage/kcms/deepin-kcm_kwinrules/
%{_datadir}/kpackage/kcms/deepin-kcm_virtualkeyboard/
%{_datadir}/krunner/dbusplugins/deepin-kwin-runner-windows.desktop
%{_datadir}/kservices5/deepin-*.desktop
%{_datadir}/kservices5/deepin-kwin/kwin4_decoration_qml_plastik.desktop
%{_datadir}/kservicetypes5/deepin-*.desktop
%{_datadir}/qlogging-categories5/*categories

%{_libdir}/kconf_update_bin/deepin-kwin5_update_default_rules
%{_libdir}/libdeepin-kcmkwincommon.so.5*
%{_libdir}/libdeepin-kwin.so.5*
%{_libdir}/libdeepin-kwineffects.so.13
%{_libdir}/libdeepin-kwineffects.so.5.24.3
%{_libdir}/libdeepin-kwinglutils.so.13
%{_libdir}/libdeepin-kwinglutils.so.5.24.3
%{_libdir}/libdeepin-kwinxrenderutils.so.13
%{_libdir}/libdeepin-kwinxrenderutils.so.5.24.3
%{_libexecdir}/deepin-kwin*

%{_qt5_plugindir}/deepin-kcm_*.so
%{_qt5_plugindir}/deepin-kwin/
%{_qt5_plugindir}/deepin-kwincompositing.so
%{_qt5_plugindir}/kcms/
%{_qt5_plugindir}/kpackage/
%{_qt5_plugindir}/org.kde.deepin-kwin.platforms/
%{_qt5_plugindir}/org.kde.deepin-kwin.waylandbackends/
%{_qt5_plugindir}/org.kde.kdecoration2/
%{_qt5_qmldir}/org/deepin/kwin/
%{_qt5_qmldir}/org/kde/deepin-kwin/

%{_datadir}/translations/popupmenu/
%dir %{_datadir}/doc/HTML
%{_datadir}/doc/HTML/*/dcontrol/

%files devel
%{_includedir}/deepin_*.h
%{_libdir}/libdeepin-*.so
%{_libdir}/cmake/DeepinKWinDBusInterface/
%{_libdir}/cmake/DeepinKWinEffects/
%{_datadir}/dbus-1/interfaces/*.xml

%changelog
%autochangelog
