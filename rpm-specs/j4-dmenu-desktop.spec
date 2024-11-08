Name:           j4-dmenu-desktop
Version:        3.1
Release:        %autorelease
Summary:        Generic menu for desktop managers
# Automatically converted from old format: GPLv3 - review is highly recommended.
License:        GPL-3.0-only
URL:            https://github.com/enkore/j4-dmenu-desktop
Source0:        https://github.com/enkore/%{name}/archive/r%{version}/%{name}-r%{version}.tar.gz
BuildRequires:  meson
BuildRequires:  catch-devel spdlog-devel
BuildRequires:  gcc-c++

%description
%{name} is a replacement for i3-dmenu-desktop.
It's purpose is to find .desktop files and offer you a menu to start an
application using dmenu.  It should work just fine on about any desktop
environment.  You can also execute shell commands using it.

%prep
%autosetup -n %{name}-r%{version}

%build
%meson
%meson_build

%install
%meson_install
install -d %{buildroot}%{_mandir}/man1
cp %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/j4-dmenu-desktop
%{_datadir}/fish/vendor_completions.d/j4-dmenu-desktop.fish
%{_datadir}/zsh/site-functions/_j4-dmenu-desktop

%changelog
%autochangelog
