Name:           deepin-screensaver
Version:        5.0.19
Release:        %autorelease
Summary:        Screensaver Tool
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/deepin-screensaver
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(dtkcore)
BuildRequires:  pkgconfig(dtkwidget)
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  cmake(DWayland)
BuildRequires:  cmake(KF5I18n)
BuildRequires:  opencv-devel
BuildRequires:  deepin-desktop-base

BuildRequires:  desktop-file-utils

Requires:       xscreensaver-extras
Requires:       xscreensaver-gl-extras

%description
Deepin screensaver viewer and tools.

%prep
%autosetup -p1

sed -i 's|lrelease|lrelease-qt5|' \
    customscreensaver/deepin-custom-screensaver/generate_translations.sh \
    src/generate_translations.sh

sed -i 's|lupdate|lupdate-qt5|' src/update_translations.sh

sed -i 's|/etc/os-version|/etc/uos-version|' common.pri

sed -i 's|/etc/deepin-screensaver/$${TARGET}/|/usr/share/applications|' \
    customscreensaver/deepin-custom-screensaver/deepin-custom-screensaver.pro

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}
%find_lang deepin-custom-screensaver --with-qt
%find_lang deepin-screensaver --with-qt
rm %{buildroot}%{_datadir}/deepin-custom-screensaver/translations/deepin-custom-screensaver.qm
rm %{buildroot}%{_datadir}/deepin-screensaver/translations/deepin-screensaver.qm

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f deepin-screensaver.lang -f deepin-custom-screensaver.lang
%doc README.md
%license LICENSE.txt
%{_bindir}/deepin-screensaver
%{_datadir}/dbus-1/interfaces/com.deepin.ScreenSaver.xml
%{_datadir}/dbus-1/services/com.deepin.ScreenSaver.service
%{_datadir}/applications/deepin-custom-screensaver.desktop
%{_datadir}/dsg/configs/org.deepin.screensaver/
%{_prefix}/lib/deepin-screensaver/

%changelog
%autochangelog
