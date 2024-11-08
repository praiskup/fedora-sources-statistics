Name:		converseen
Version:	0.12.2.4
Release:	%autorelease
Summary:	A batch image conversion tool written in C++ with Qt5 and Magick++
# Automatically converted from old format: GPLv3 - review is highly recommended.
License:	GPL-3.0-only
URL:		http://converseen.sf.net/
Source0:	http://downloads.sourceforge.net/converseen/%{name}-%{version}.tar.bz2
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	ImageMagick-devel
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-linguist

%description
Converseen is a batch image conversion tool and resizer written in C++ with Qt5
and Magick++.  Converseen allows you to convert images in more than 100
different formats!

%prep
%autosetup

%build
%cmake
%cmake_build

%install
%cmake_install
desktop-file-validate %{buildroot}/%{_datadir}/applications/net.fasterland.%{name}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/applications/net.fasterland.%{name}.desktop
%{_datadir}/converseen
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/kio/servicemenus/%{name}_import.desktop

%changelog
%autochangelog
