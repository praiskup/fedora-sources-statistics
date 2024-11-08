%global srcname Projecteur

Name:           projecteur
Version:        0.10
Release:        %autorelease
Summary:        Virtual pointer for the Logitech Spotlight presentation remote

License:        MIT
URL:            https://github.com/jahnf/Projecteur
Source:         %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtquickcontrols2-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  systemd-devel

Requires:       hicolor-icon-theme
Requires:       systemd-udev
Recommends:     bash-completion
Suggests:       gnome-shell-extension-appindicator

%description
Projecteur is a virtual laser pointer for use with inertial pointers such as
the Logitech Spotlight. Projecteur can show a colored dot, a highlighted circle
or a zoom effect to act as a pointer. The location of the pointer moves in
response to moving the handheld pointer device. The effect is much like that of
a traditional laser pointer, except that it is captured by recording software
and works across multiple screens.

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
%cmake -D CMAKE_INSTALL_UDEVRULESDIR="%{_udevrulesdir}"
%cmake_build

%install
%cmake_install

%check
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
desktop-file-validate \
  %{buildroot}/%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE.md
%doc README.md doc
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.svg
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/%{name}.metainfo.xml
%{_udevrulesdir}/55-projecteur.rules

%changelog
%autochangelog
