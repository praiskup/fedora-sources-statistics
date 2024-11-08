Summary:       X11 utility to view and edit application resources
Name:          editres
Version:       1.0.9
Release:       %autorelease
License:       MIT
URL:           https://www.x.org
Source0:       https://www.x.org/pub/individual/app/%{name}-%{version}.tar.xz
Patch01:       editres-1.0.6-format-security.patch
BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xaw7)
BuildRequires: pkgconfig(xmu)
BuildRequires: pkgconfig(xorg-macros) >= 1.8
BuildRequires: pkgconfig(xt)
BuildRequires: libxkbfile-devel
Obsoletes:     xorg-x11-resutils < 7.7-9
%description
editres is a tool that allows users and application developers to view
the full widget hierarchy of any Xt Toolkit application that speaks the
Editres protocol  In addition, editres will help the user construct
resource specifications, allow the user to apply the resource to
the application and view the results dynamically.

%prep
%autosetup

%build
%configure --disable-silent-rules --disable-xprint
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/X11/app-defaults/Editres
%{_datadir}/X11/app-defaults/Editres-color

%changelog
%autochangelog
