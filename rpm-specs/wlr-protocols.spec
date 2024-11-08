%global forgeurl https://gitlab.freedesktop.org/wlroots/wlr-protocols
%global date 20240126
%global commit 2b8d43325b7012cc3f9b55c08d26e50e42beac7d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           wlr-protocols
Version:        0^%{date}git%{shortcommit}
Release:        %autorelease
Summary:        Wayland protocols designed for use in wlroots (and other compositors)
License:        MIT
URL:            %{forgeurl}
Source0:        %{forgeurl}/-/archive/%{commit}/%{name}-%{commit}.tar.bz2

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  /usr/bin/wayland-scanner

%description
Wayland protocols designed for use in wlroots (and other compositors).

%package        devel
Summary:        Wayland protocols designed for use in wlroots (and other compositors)

%description    devel
Wayland protocols designed for use in wlroots (and other compositors).

%prep
%autosetup -p1 -n %{name}-%{commit}

%build
%make_build

%install
%make_install

%files devel
%{_datadir}/pkgconfig/wlr-protocols.pc
%{_datadir}/wlr-protocols/

%changelog
%autochangelog
