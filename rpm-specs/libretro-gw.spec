%global forgeurl https://github.com/libretro/%{corename}-libretro
%global commit 0ecff52b11c327af52b22ea94b268c90472b6732
%global corename gw

Name:           libretro-%{corename}
Version:        0
%forgemeta
Release:        7.%autorelease
Summary:        Libretro core for Game & Watch simulators

License:        zlib
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  gcc-c++
BuildRequires:  make

Supplements:    retroarch

Provides:       bundled(lua) = 5.3.0

%description
gw-libretro is a libretro core that runs Game & Watch simulators.

It runs simulators converted from source code for the games available at
MADrigal. Each simulator is converted with pas2lua, which was written
specifically for this purpose, and uses bstree, which was also specifically
written to obfuscate the generated Lua source code as per MADrigal's request.


%prep
%forgeautosetup -p1


%build
%set_build_flags
%make_build


%install
install -m 0755 -Dp %{corename}_libretro.so %{buildroot}%{_libdir}/libretro/%{corename}_libretro.so


%files
%license LICENSE
%doc README.md
%{_libdir}/libretro/


%changelog
%autochangelog
