Summary:   GTK+ 3 support library for colord
Name:      colord-gtk
Version:   0.3.1
Release:   %autorelease
License:   LGPL-2.1-or-later
URL:       http://www.freedesktop.org/software/colord/
Source0:   http://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz

BuildRequires: meson
BuildRequires: docbook5-style-xsl
BuildRequires: gettext >= 0.19.8
BuildRequires: glib2-devel
BuildRequires: colord-devel >= 0.1.23
BuildRequires: lcms2-devel >= 2.2
BuildRequires: gobject-introspection-devel
BuildRequires: vala
BuildRequires: gtk3-devel
BuildRequires: gtk4-devel
BuildRequires: gtk-doc

%description
colord-gtk is a support library for colord and provides additional
functionality that requires GTK+.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package -n colord-gtk4
Summary:  GTK 4 support library for colord

%description -n colord-gtk4
colord-gtk is a support library for colord and provides additional
functionality that requires GTK. This package contains the GTK 4
build of colord-gtk.

%package -n colord-gtk4-devel
Summary:  Development package for colord-gtk4
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description -n colord-gtk4-devel
Files for GTK 4 development with %{name}4.

%prep
%autosetup -p1

%build
%meson -Ddocs=true -Dgtk2=false -Dman=true -Dtests=false -Dvapi=true
%meson_build

%install
%meson_install

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc README AUTHORS NEWS COPYING
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_libdir}/libcolord-gtk.so.*
%{_libdir}/girepository-1.0/ColordGtk-1.0.typelib

%files -n colord-gtk4
%{_libdir}/libcolord-gtk4.so.*

%files devel
%{_libdir}/libcolord-gtk.so
%{_libdir}/pkgconfig/colord-gtk.pc
%dir %{_includedir}/colord-1
%{_includedir}/colord-1/colord-gtk.h
%dir %{_includedir}/colord-1/colord-gtk
%{_includedir}/colord-1/colord-gtk/*.h
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/ColordGtk-1.0.gir
%doc %{_datadir}/gtk-doc/html/colord-gtk
%{_datadir}/vala/vapi/colord-gtk.vapi
%{_datadir}/vala/vapi/colord-gtk.deps
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html

%files -n colord-gtk4-devel
%{_libdir}/libcolord-gtk4.so
%{_libdir}/pkgconfig/colord-gtk4.pc
# Requires the base -devel package for headers. No GTK 4 .gir nor VAPI yet.


%changelog
%autochangelog
