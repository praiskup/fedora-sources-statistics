%global rdnn    org.heliumos.bootc_gtk

Name:           bootc-gtk
Version:        0.3
Release:        %autorelease
Summary:        A GTK4 interface for bootc

License:        GPL-2.0-or-later
URL:            https://codeberg.org/HeliumOS/bootc-gtk
BuildArch:      noarch

Source:         %{url}/archive/%{version}.tar.gz#/bootc-gtk.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  python3-devel

Requires:       bootc
Requires:       gtk4
Requires:       hicolor-icon-theme
# /usr/lib64/girepository-1.0/Adw-1.typelib is needed for `gi.require_version('Adw', '1')` in src/main.py
Requires:       libadwaita
Requires:       python3-gobject


%description
A GTK4 interface for bootc.


%prep
%autosetup -n bootc-gtk
sed -r \
    -e '/\b(glib_compile_schemas|gtk_update_icon_cache|update_desktop_database)\b/ s/true/false/' \
    -i meson.build


%build
%meson
%meson_build


%install
%meson_install
%py3_shebang_fix %{buildroot}%{_bindir}/%{name}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{rdnn}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{rdnn}.metainfo.xml


%files
%license LICENSE.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{rdnn}.desktop
%{_datadir}/glib-2.0/schemas/%{rdnn}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{rdnn}*.svg
%{_metainfodir}/%{rdnn}.metainfo.xml



%changelog
%autochangelog
