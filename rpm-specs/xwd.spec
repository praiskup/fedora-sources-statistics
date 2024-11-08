Name:       xwd
Version:    1.0.9
Release:    %autorelease
Summary:    Dump an X window to file

License:    MIT-open-group AND HPND-sell-variant
URL:        https://www.x.org
Source0:    https://www.x.org/pub/individual/app/%{name}-%{version}.tar.xz

BuildRequires:  automake libtool
BuildRequires:  gcc make
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8

Obsoletes:  xorg-x11-apps < 7.7-31

%description
Xwd is an X Window System window dumping utility. Xwd allows X users to
store window images in a specially formatted dump file. This file can then
be read by various other X utilities for redisplay, printing, editing,
formatting, archiving, image processing, etc.

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
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
