%global glib2_version 2.45.8
%global json_glib_version 1.1.2
%global gdk_pixbuf_version 2.31.5

Summary:   Library for AppStream metadata
Name:      libappstream-glib
Version:   0.8.3
Release:   %autorelease
License:   LGPL-2.1-or-later
URL:       http://people.freedesktop.org/~hughsient/appstream-glib/
Source0:   http://people.freedesktop.org/~hughsient/appstream-glib/releases/appstream-glib-%{version}.tar.xz

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: docbook-utils
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: gperf
BuildRequires: libarchive-devel
BuildRequires: libcurl-devel
BuildRequires: gdk-pixbuf2-devel >= %{gdk_pixbuf_version}
BuildRequires: gtk3-devel
BuildRequires: gettext
BuildRequires: libuuid-devel
BuildRequires: json-glib-devel >= %{json_glib_version}
BuildRequires: meson

# for the builder component
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: pango-devel
BuildRequires: rpm-devel

# for the manpages
BuildRequires: libxslt
BuildRequires: docbook-style-xsl

# Make sure we pull in the minimum required versions
Requires: gdk-pixbuf2%{?_isa} >= %{gdk_pixbuf_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: json-glib%{?_isa} >= %{json_glib_version}

# no longer required
Obsoletes: appdata-tools < 0.1.9
Provides: appdata-tools

# Removed in F30
Obsoletes: libappstream-glib-builder-devel < 0.7.15

# this is not a library version
%define as_plugin_version               5

%description
This library provides GObjects and helper methods to make it easy to read and
write AppStream metadata. It also provides a simple DOM implementation that
makes it easy to edit nodes and convert to and from the standardized XML
representation.

%package devel
Summary: GLib Libraries and headers for appstream-glib
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GLib headers and libraries for appstream-glib.

%package builder
Summary: Library and command line tools for building AppStream metadata
Requires: %{name}%{?_isa} = %{version}-%{release}
Recommends: pngquant

%description builder
This library and command line tool is used for building AppStream metadata
from a directory of packages.

%prep
%autosetup -p1 -n appstream-glib-%{version}

%build
%meson \
    -Dgtk-doc=true \
    -Ddep11=false
%meson_build

%install
%meson_install

%find_lang appstream-glib

%ldconfig_scriptlets
%ldconfig_scriptlets builder

%files -f appstream-glib.lang
%license COPYING
%doc README.md AUTHORS NEWS
%{_libdir}/libappstream-glib.so.8*
%{_libdir}/girepository-1.0/*.typelib
%{_bindir}/appstream-util
%{_bindir}/appstream-compose
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/appstream-util
%{_mandir}/man1/appstream-util.1.gz
%{_mandir}/man1/appstream-compose.1.gz

%files devel
%{_libdir}/libappstream-glib.so
%{_libdir}/pkgconfig/appstream-glib.pc
%dir %{_includedir}/libappstream-glib
%{_includedir}/libappstream-glib/*.h
%{_datadir}/gtk-doc/html/appstream-glib
%{_datadir}/gir-1.0/AppStreamGlib-1.0.gir
%{_datadir}/aclocal/*.m4
%{_datadir}/installed-tests/appstream-glib/*.test
%{_datadir}/gettext/its/appdata.its
%{_datadir}/gettext/its/appdata.loc

%files builder
%license COPYING
%{_bindir}/appstream-builder
%{_datadir}/bash-completion/completions/appstream-builder
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_appdata.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_desktop.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_font.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_gettext.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_hardcoded.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_icon.so
%{_libdir}/asb-plugins-%{as_plugin_version}/libasb_plugin_shell_extension.so
%{_mandir}/man1/appstream-builder.1.gz

%changelog
%autochangelog
