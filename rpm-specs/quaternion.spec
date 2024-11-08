%global appid       com.github.quaternion
%global forgeurl    https://github.com/quotient-im/Quaternion
%global tag         %{version}

Name:       quaternion
Version:    0.0.96.1
Release:    %autorelease -p -e rc1

%forgemeta

Summary:    A Qt-based IM client for Matrix
License:    GPL-3.0-or-later
URL:        %{forgeurl}
Source0:    %{forgesource}

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib

BuildRequires: cmake(Olm)
BuildRequires: cmake(QuotientQt6)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: cmake(Qt6Multimedia)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(Qt6QuickWidgets)
BuildRequires: cmake(Qt6Keychain)

Requires:       hicolor-icon-theme

%description
Quaternion is a cross-platform desktop IM client for the Matrix protocol.

%prep
%forgesetup

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_INTREE_LIBQMC=NO
%cmake_build

%install
%cmake_install
%find_lang %{name} --with-qt
cp -p linux/%{appid}.appdata.xml %{buildroot}%{_metainfodir}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{appid}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appid}.appdata.xml

%files -f %{name}.lang
%license LICENSES/*
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_metainfodir}/%{appid}.appdata.xml

%changelog
%autochangelog
