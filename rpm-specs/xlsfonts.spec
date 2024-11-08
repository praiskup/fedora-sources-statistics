Summary:    X font list utility
Name:       xlsfonts
Version:    1.0.8
Release:    %autorelease
License:    MIT
URL:        http://www.x.org
Source0:    https://www.x.org/pub/individual/app/%{name}-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig(x11)
Obsoletes: xorg-x11-utils < 7.5-39

%description
xlsfonts lists the fonts available on an X server.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%files
%doc README.md
%license COPYING
%{_bindir}/xlsfonts
%{_mandir}/man1/xlsfonts.1*

%changelog
%autochangelog
