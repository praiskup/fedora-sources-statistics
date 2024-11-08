Summary:    X video extension query utility
Name:       xvinfo
Version:    1.1.5
Release:    %autorelease
License:    MIT
URL:        https://www.x.org
Source0:    https://www.x.org/pub/individual/app/%{name}-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xv)
Obsoletes: xorg-x11-utils < 7.5-39

%description
xvinfo displays information about the XVideo extension on an X server.

%prep
%setup -q

%build
%configure
%make_build

%install
%make_install

%files
%doc README.md
%license COPYING
%{_bindir}/xvinfo
%{_mandir}/man1/xvinfo.1*

%changelog
%autochangelog
