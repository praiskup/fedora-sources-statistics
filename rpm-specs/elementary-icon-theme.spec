%global srcname icons
%global appname io.elementary.icons

Name:           elementary-icon-theme
Summary:        Icons from the Elementary Project
Version:        8.1.0
Release:        %autorelease
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:        GPL-3.0-or-later

URL:            https://github.com/elementary/icons
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  gettext
BuildRequires:  libappstream-glib
# /usr/bin/rsvg-convert
BuildRequires:  librsvg2-tools
BuildRequires:  meson
BuildRequires:  xcursorgen

%description
This is an icon theme designed to be smooth, sexy, clear, and efficient.


%package        gimp-palette
Summary:        Icons from the Elementary Project (GIMP palette)
Requires:       %{name} = %{version}-%{release}
Requires:       gimp
%if ! 0%{?fedora} || 0%{?fedora} >= 41
ExcludeArch:    s390x
%endif

%description    gimp-palette
This is an icon theme designed to be smooth, sexy, clear, and efficient.

This package contains a palette file for the GIMP.


%package        inkscape-palette
Summary:        Icons from the Elementary Project (inkscape palette)
Requires:       %{name} = %{version}-%{release}
Requires:       inkscape

%description    inkscape-palette
This is an icon theme designed to be smooth, sexy, clear, and efficient.

This package contains a palette file for inkscape.


%prep
%autosetup -n %{srcname}-%{version} -p1


%build
# Clean up executable permissions
for i in $(find -type f -executable); do
    chmod a-x $i;
done

%meson -Dvolume_icons=false
%meson_build


%install
%meson_install

# Create icon cache file
touch %{buildroot}/%{_datadir}/icons/elementary/icon-theme.cache


%check
# ignore validation until appstream-glib knows the "icon-theme" component type
appstream-util validate-relax --nonet \
    %{buildroot}/%{_datadir}/metainfo/%{appname}.appdata.xml || :


%transfiletriggerin -- %{_datadir}/icons/elementary
gtk-update-icon-cache --force %{_datadir}/icons/elementary &>/dev/null || :

%transfiletriggerpostun -- %{_datadir}/icons/elementary
gtk-update-icon-cache --force %{_datadir}/icons/elementary &>/dev/null || :


%files
%doc README.md
%license COPYING
%{_datadir}/icons/elementary/*@2x
%{_datadir}/icons/elementary/*@3x
%{_datadir}/metainfo/io.elementary.icons.metainfo.xml


%dir %{_datadir}/icons/elementary
%ghost %{_datadir}/icons/elementary/icon-theme.cache

%{_datadir}/icons/elementary/actions/
%{_datadir}/icons/elementary/apps/
%{_datadir}/icons/elementary/categories/
%{_datadir}/icons/elementary/cursors/
%{_datadir}/icons/elementary/devices/
%{_datadir}/icons/elementary/emblems/
%{_datadir}/icons/elementary/emotes/
%{_datadir}/icons/elementary/mimes/
%{_datadir}/icons/elementary/places/
%{_datadir}/icons/elementary/status/

%{_datadir}/icons/elementary/cursor.theme
%{_datadir}/icons/elementary/index.theme


%files gimp-palette
%{_datadir}/gimp/2.0/palettes/elementary.gpl

%files inkscape-palette
%{_datadir}/inkscape/palettes/elementary.gpl


%changelog
%autochangelog
