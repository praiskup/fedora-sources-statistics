%global repo dde-control-center

Name:           deepin-control-center
Version:        6.0.62
Release:        %autorelease
Summary:        New control center for Linux Deepin
License:        LGPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-control-center
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
# adopted from Arch Linux
Patch0:         https://gitlab.archlinux.org/archlinux/packaging/packages/deepin-control-center/-/raw/main/deepin-control-center-systeminfo-deepin-icon.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5Test)
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
# provides qhelpgenerator
BuildRequires:  qt5-doctools

BuildRequires:  cmake(DtkCore)
BuildRequires:  cmake(DtkWidget)
BuildRequires:  cmake(DtkDConfig)

BuildRequires:  cmake(GTest)
BuildRequires:  cmake(PolkitQt5-1)

BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(libdeepin_pw_check)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(dareader)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-client)

BuildRequires:  libicu-devel

# provides /usr/bin/deepin-desktop-ts-convert
BuildRequires:  deepin-desktop-base
BuildRequires:  doxygen

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       %{name}-lib%{?_isa} = %{version}-%{release}
Requires:       deepin-account-faces
Requires:       deepin-api
Requires:       deepin-daemon
Requires:       deepin-qt5integration
Requires:       startdde
Requires:       deepin-network-core

%description
New control center for Linux Deepin.

%package        lib
Summary:        Shared library files for %{name}

%description    lib
This package contains shared library files for %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-lib%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1 -n %{repo}-%{version}

sed -i 's|lrelease|lrelease-qt5|g' misc/translate_generation.sh
sed -i 's|lupdate|lupdate-qt5|g' misc/lupdate.sh

sed -i 's|systemsettings|preferences-system|' misc/org.deepin.dde.controlcenter.metainfo.xml

%build
%cmake \
    -GNinja \
    -DBUILD_TESTING=OFF \
    -DDISABLE_AUTHENTICATION=ON \
    -DQCH_INSTALL_DESTINATION=%{_qt5_docdir} \
%cmake_build

%install
%cmake_install
%find_lang datetime_country --with-qt
%find_lang datetime_language --with-qt
%find_lang dde-control-center --with-qt
%find_lang keyboard_language --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
# appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%files -f datetime_country.lang -f datetime_language.lang -f dde-control-center.lang -f keyboard_language.lang
%license LICENSE
%doc README.md
%{_bindir}/dde-control-center
%{_datadir}/applications/org.deepin.dde.control-center.desktop
%{_datadir}/dbus-1/services/*.service
%{_userunitdir}/org.deepin.dde.control-center.service
%{_libdir}/dde-grand-search-daemon/plugins/searcher/org.deepin.dde-grand-search.dde-control-center-setting.conf
%dir %{_libdir}/dde-control-center
%dir %{_libdir}/dde-control-center/modules
%{_libdir}/dde-control-center/modules/libdcc-*.so
%dir %{_datadir}/dde-control-center
%{_datadir}/dde-control-center/developdocument.html
%{_datadir}/dsg/configs/org.deepin.dde.control-center/*.json
%{_datadir}/dsg/configs/org.deepin.region-format.json
%{_datadir}/metainfo/org.deepin.dde.controlcenter.metainfo.xml

%files lib
%{_libdir}/libdcc-interface.so.6*
%{_libdir}/libdcc-widgets.so.6*

%files devel
%{_libdir}/libdcc-interface.so
%{_libdir}/libdcc-widgets.so
%{_includedir}/dde-control-center/
%{_libdir}/cmake/DdeControlCenter/
%{_qt5_docdir}/dde-control-center.qch

%changelog
%autochangelog
