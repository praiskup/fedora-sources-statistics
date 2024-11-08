%bcond check 1
%global debug_package %{nil}

# https://github.com/linuxdeepin/deepin-desktop-schemas
%global goipath         github.com/linuxdeepin/deepin-desktop-schemas
Version:                6.0.6
%global tag             %{version}

%gometa -L

%global common_description %{expand:
GSettings deepin desktop-wide schemas.}

Name:           deepin-desktop-schemas
Release:        %autorelease
Summary:        GSettings deepin desktop-wide schemas

License:        GPL-3.0-or-later
URL:            %{gourl}
Source:         %{gosource}

%if %{with check}
# For glib-compile-schemas
BuildRequires:  glib2
%endif

Requires:       dconf
Requires:       deepin-gtk-theme
Requires:       deepin-icon-theme
Requires:       deepin-sound-theme
Obsoletes:      deepin-artwork-themes <= 15.12.4

%description
%{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

# fix default background url
sed -i "s#/usr/share/backgrounds/default_background.jpg#/usr/share/backgrounds/deepin/desktop.jpg#" \
    overrides/common/com.deepin.wrap.gnome.desktop.override \
    schemas/com.deepin.dde.appearance.gschema.xml

sed -i 's|python|python3|' Makefile tools/overrides.py
# connectivity check uri copy from /usr/lib/NetworkManager/conf.d/20-connectivity-fedora.conf
sed -i "s#'http://detect.uniontech.com', 'http://detectportal.deepin.com'#'http://fedoraproject.org/static/hotspot.txt'#" \
    schemas/com.deepin.dde.network-utils.gschema.xml
grep uniontech schemas/com.deepin.dde.network-utils.gschema.xml && exit 1 || :

%generate_buildrequires
%go_generate_buildrequires

%build
mkdir -p bin
%gobuild -o bin/override_tool tools/override/*.go

mkdir -p result
find schemas -name "*.xml" -exec cp {} result \;
bin/override_tool -arch x86

%install
%make_install PREFIX=%{_prefix}

%if %{with check}
%check
%gocheck
make test
%endif

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/deepin-appstore/
%{_datadir}/deepin-app-store/
%{_datadir}/deepin-desktop-schemas/

%changelog
%autochangelog
