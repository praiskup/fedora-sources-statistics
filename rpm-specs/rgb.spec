Name:       rgb
Version:    1.1.0
Release:    %autorelease
Summary:    X color name database

License:    MIT-open-group
URL:        https://www.x.org
Source0:    https://www.x.org/pub/individual/app/%{name}-%{version}.tar.xz

BuildRequires:  automake libtool
BuildRequires:  gcc make
BuildRequires:  pkgconfig(xproto)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8

Obsoletes:  xorg-x11-server-utils < 7.7-40

%description
This package includes both the list mapping X color names to RGB values
(rgb.txt) and, if configured to use a database for color lookup, the
rgb program to convert the text file into the binary database format.

%prep
%autosetup

%build
autoreconf -v --install
%configure --disable-silent-rules
%make_build

%install
%make_install

%files
%{_bindir}/showrgb
%{_datadir}/X11/rgb.txt
%{_mandir}/man1/showrgb.1*

%changelog
%autochangelog
