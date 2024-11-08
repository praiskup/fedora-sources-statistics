%global forgeurl https://github.com/toppk/%{name}
%dnl %global tag v%{version}
%global commit 91173774684eb554a8c6249f9c1e012dc58fd668
%global shortname openweather
%global uuid %{shortname}-extension@jenslody.de

Name:           gnome-shell-extension-%{shortname}
Version:        121
%forgemeta
Release:        %autorelease
Summary:        Display weather information for any location on Earth
BuildArch:      noarch

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}
# Port to Gnome 46
Patch:          %{url}/pull/14.patch#/Port-to-Gnome-46.patch

BuildRequires:  gettext-devel
BuildRequires:  glib2-devel
BuildRequires:  make
# The version of gnome-common in CentOS7 is only 3.7.4
BuildRequires:  gnome-common >= 3.7.4

Requires:       gnome-shell >= 43

%description
OpenWeather (%uuid) is a simple extension for
displaying weather conditions and forecasts for any location on Earth in the
GNOME Shell. It provides support for multiple locations with editable names
using coordinates to store the locations, a beautiful layout, and more.
Weather data is fetched from OpenWeatherMap including 3 hour forecasts for up
to 5 days.

After completing installation, restart GNOME Shell (Alt+F2, r, Enter) and
enable the extension through the gnome-extensions app or via terminal:

  $ gnome-shell-extension-tool -e %uuid


%prep
%forgeautosetup -p1


%build
%make_build


%install
%make_install
%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/gnome-shell/extensions/%{uuid}/


%changelog
%autochangelog
