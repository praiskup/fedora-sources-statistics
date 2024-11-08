%global forgeurl https://github.com/oferkv/phototonic
%global version0 2.1.12
%global commit0  12552ece9564b1452606d653be67478ec6573ca1

%forgemeta

Name:           phototonic
Version:        %forgeversion
Release:        %autorelease
Summary:        Image viewer and organizer

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source:         %{forgesource}


BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(exiv2)
BuildRequires:  qt5-linguist

%description
Phototonic is a fast and functional image viewer and organizer, inspired by the
traditional image viewer design (i.e. thumbnails and viewer layouts).


%prep
%forgesetup


%build
%{qmake_qt5}
%{make_build}


%install
%{make_install} INSTALL_ROOT=%{buildroot}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_metainfodir}/%{name}.appdata.xml

%changelog
%autochangelog
