%global altname ZeGrapher

Name:           zegrapher
Summary:        Free and opensource math graphing software
Version:        3.1.1
Release:        %autorelease
License:        GPL-3.0-or-later

URL:            https://www.zegrapher.com/
Source0:        https://github.com/AdelKS/%{altname}/archive/v%{version}/%{altname}-%{version}.tar.gz
# Grab ZeGrapher.appdata.xml from the appdata dir
Patch0:         https://patch-diff.githubusercontent.com/raw/AdelKS/ZeGrapher/pull/19.patch#/0001-Grab-ZeGrapher.appdata.xml-from-the-appdata-dir.patch

BuildRequires: make
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5WebKit)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%description
ZeGrapher is a plotting program for functions, sequences, parametric equations,
and tabular data. It has been designed to be as easy to use as possible.

ZeGrapher supports importing and exporting of tabular data from and to CSV files
and polynomial (regression) fits, plotting of tangents (the point can be
selected interactively). Calculation and plotting of derivatives and integrals
is also possible.

Plots can be exported in various image formats and as PDF files.

%prep
%autosetup -p1 -n %{altname}-%{version}
sed -i 's|^QMAKE_LFLAGS_RELEASE = -s|QMAKE_LFLAGS_RELEASE =|' ZeGrapher.pro

%build
mkdir build && cd build
%qmake_qt5 ../ PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot} -C build

%find_lang %{altname} --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{altname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{altname}.appdata.xml

%files -f %{altname}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{altname}
%{_metainfodir}/%{altname}.appdata.xml
%{_datadir}/applications/%{altname}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{altname}.png
%dir %{_datadir}/%{altname}

%changelog
%autochangelog
