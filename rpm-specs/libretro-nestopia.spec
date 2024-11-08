%global forgeurl https://github.com/libretro/%{corename}
%global commit b99ede358b2219602443e7f414eabf81e17da244
%global corename nestopia

Name:           libretro-%{corename}
Version:        0
%forgemeta
Release:        0.9.%autorelease
Summary:        Nestopia emulator with libretro interface

License:        GPL-2.0-only
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://raw.githubusercontent.com/flathub/org.gnome.Games/master/libretro-cores/%{corename}.libretro

BuildRequires:  gcc-c++
BuildRequires:  make

Supplements:    gnome-games
Supplements:    retroarch

%description
%{summary}.


%prep
%forgeautosetup -p1


%build
%set_build_flags
%make_build -C libretro GIT_VERSION=%{shortcommit}


%install
%make_install         \
    -C libretro       \
    libdir=%{_libdir} \
    prefix=%{_prefix} \
    %{nil}
install -Dp -m0644 %{SOURCE1} %{buildroot}%{_libdir}/libretro/%{corename}.libretro


%files
%license COPYING
%{_libdir}/libretro/


%changelog
%autochangelog
