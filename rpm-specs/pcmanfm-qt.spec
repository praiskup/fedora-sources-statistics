Name:           pcmanfm-qt
Version:        2.0.0
Release:        %autorelease
Summary:        LxQt file manager PCManFM

License:        GPL-2.0-or-later
URL:            https://lxqt-project.org
Source0:        https://github.com/lxde/pcmanfm-qt/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(LayerShellQt)
BuildRequires:  lxqt-build-tools
BuildRequires:  pkgconfig(exiv2)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libfm)
BuildRequires:  pkgconfig(libfm-qt6)
BuildRequires:  pkgconfig(libmenu-cache)
BuildRequires:  pkgconfig(lxqt) >= 1.0.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  lxqt-menu-data
%if 0%{?el7}
BuildRequires:  devtoolset-7-gcc-c++
%endif
Requires:       lxqt-sudo

%if 0%{?fedora}
Requires:       desktop-backgrounds-compat
%endif
Obsoletes:      pcmanfm-qt5 < 0.9.0
Provides:       pcmanfm-qt5 = %{version}-%{release}
Obsoletes:      pcmanfm-qt4 <= 0.9.0
Obsoletes:      pcmanfm-qt-common <= 0.9.0

%if 0%{?fedora}
# gvfs is optional depencency at runtime, so we add a weak dependency here
Recommends:     gvfs
# configuration patched to use qterminal instead as the default terminal emulator but allow to use others
Requires:       qterminal
%endif

%description
PCManFM-Qt is a Qt-based file manager which uses GLib for file management. It
was started as the Qt port of PCManFM, the file manager of LXDE.

PCManFM-Qt is used by LXQt for handling the desktop. Nevertheless, it can also
be used independently of LXQt and under any desktop environment.

%package        l10n
Summary:        Translations for pcmanfm-qt
BuildArch:      noarch
Requires:       pcmanfm-qt = %{?epoch:%{epoch}:}%{version}-%{release}

%description    l10n
This package provides translations for the pcmanfm-qt package.

%prep
%autosetup -p1
sed '/Wallpaper=/c\Wallpaper=\%{datadir}\/backgrounds\/default.png' config/pcmanfm-qt/lxqt/settings.conf.in

%build
%if 0%{?el7}
scl enable devtoolset-7 - <<\EOF
%endif
%cmake
%cmake_build

%if 0%{?el7}
EOF
%endif

%install
%cmake_install
for dfile in pcmanfm-qt-desktop-pref pcmanfm-qt; do
    desktop-file-edit \
        --remove-category=LXQt --add-category=X-LXQt \
        --remove-category=Help --add-category=X-Help \
        --remove-only-show-in=LXQt \
        %{buildroot}/%{_datadir}/applications/${dfile}.desktop
done

%find_lang %{name} --with-qt

%if 0%{?el7}
%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
%endif


%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-desktop-pref.desktop
%{_mandir}/man1/%{name}.*
%{_sysconfdir}/xdg/autostart/lxqt-desktop.desktop
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/scalable/apps/pcmanfm-qt.svg

%files l10n -f %{name}.lang
%doc AUTHORS CHANGELOG README.md
%dir %{_datadir}/%{name}/translations

%changelog
%autochangelog
