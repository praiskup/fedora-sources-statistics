Name:       xvidtune
Version:    1.0.4
Release:    %autorelease
Summary:    Video mode tuner for Xorg
License:    X11-distribute-modifications-variant
URL:        https://www.x.org
Source0:    https://www.x.org/pub/individual/app/%{name}-%{version}.tar.xz

BuildRequires:  automake libtool
BuildRequires:  gcc make
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xaw7)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8

Obsoletes:  xorg-x11-apps < 7.7-31

%description
xvidtune is a client interface to the X server video mode extension
(XFree86-VidModeExtension).

%prep
%autosetup

%build
autoreconf -v --install
%configure --disable-silent-rules
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/xvidtune
%{_mandir}/man1/xvidtune.1*
%{_datadir}/X11/app-defaults/Xvidtune

%changelog
%autochangelog
