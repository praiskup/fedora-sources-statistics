Name:           deepin-sound-theme
Version:        15.10.6
Release:        %autorelease
Summary:        Deepin sound theme
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/deepin-sound-theme
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make

%description
Sound files for the Deeping Desktop Environment.

%prep
%autosetup -p1

%build

%install
%make_install

%files
%doc README.md
%license LICENSE
%dir %{_datadir}/sounds/deepin/
%dir %{_datadir}/sounds/deepin/stereo/
%{_datadir}/sounds/deepin/index.theme
%{_datadir}/sounds/deepin/stereo/*.wav

%changelog
%autochangelog
