%global sdbus_version 1.3.0

Name:           xdg-desktop-portal-hyprland
Version:        1.3.6
Release:        %autorelease
Summary:        xdg-desktop-portal backend for hyprland

# xdg-desktop-portal-hyprland: BSD-3-Clause
# protocols/wlr-foreign-toplevel-management-unstable-v1.xml: HPND-sell-variant
# sdbus-cpp: LGPL-2.1-or-later WITH Qt-LGPL-exception-1.1
%if %{fedora} < 40
License:        BSD-3-Clause AND HPND-sell-variant AND LGPL-2.1-or-later WITH Qt-LGPL-exception-1.1
%else
License:        BSD-3-Clause AND HPND-sell-variant
%endif
URL:            https://github.com/hyprwm/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/Kistler-Group/sdbus-cpp/archive/v%{sdbus_version}/sdbus-%{sdbus_version}.tar.gz
Patch:          revert-c5b309.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(Qt6Widgets)
%if %{fedora} >= 40
BuildRequires:  pkgconfig(sdbus-c++)
%endif
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprutils)

Requires:       dbus-common
Requires:       dbus
# required for Screenshot portal implementation
Requires:       grim
Recommends:     hyprpicker
Requires:       xdg-desktop-portal
# required for hyprland-share-picker
Requires:       slurp
Requires:       qt6-qtwayland

Enhances:       hyprland
Supplements:    hyprland

%if %{fedora} < 40
Provides:       bundled(sdbus-cpp) = %{sdbus_version}
%endif

%description
%{summary}.


%prep
%autosetup -N
%if %{fedora} < 41
%patch -P 0 -p1
sed -i '/libpipewire/s/>=1.1.82//' CMakeLists.txt
%endif
%if %{fedora} < 40
tar -xf %{SOURCE1} -C subprojects/sdbus-cpp --strip=1
%endif


%build
%cmake -G Ninja -DBUILD_SHARED_LIBS:BOOL=OFF
%cmake_build


%install
%cmake_install


%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service


%files
%license LICENSE
%doc README.md contrib/config.sample
%{_bindir}/hyprland-share-picker
%{_libexecdir}/%{name}
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_userunitdir}/%{name}.service


%changelog
%autochangelog
