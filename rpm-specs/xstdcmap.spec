Name:           xstdcmap
Version:        1.0.5
Release:        %autorelease
Summary:        Utility to define standard colormap properties

License:        MIT
URL:            https://www.x.org
Source0:        %{url}/pub/individual/app/%{name}-%{version}.tar.xz
Source1:        %{url}/pub/individual/app/%{name}-%{version}.tar.xz.sig
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8

Obsoletes:      xorg-x11-server-utils < 7.7-40

%description
The xstdcmap utility can be used to selectively define standard colormap
properties.  It is intended to be run from a user's X startup script to
create standard colormap definitions in order to facilitate sharing of
scarce colormap resources among clients using PseudoColor visuals.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%doc ChangeLog README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
