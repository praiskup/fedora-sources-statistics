%global forgeurl https://github.com/WayfireWM/wcm

Name:           wayfire-config-manager
Version:        0.9.0
%forgemeta
Release:        %autorelease
Summary:        Wayfire Config Manager

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}

# https://github.com/WayfireWM/wcm/pull/90
Patch0:         %{forgeurl}/pull/90.patch#/appdata-fix.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  meson

BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(wayfire)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wf-config) >= 0.9.0
BuildRequires:  pkgconfig(wf-shell) >= 0.9.0

Requires:       hicolor-icon-theme

%description
%{summary}.


%prep
%forgeautosetup -p1


%build
%meson \
    -Denable_wdisplays=false \
%meson_build


%install
%meson_install


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%license LICENSE
%{_bindir}/wcm
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/wayfire/


%changelog
%autochangelog
