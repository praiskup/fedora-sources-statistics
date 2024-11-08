Name:          libdbusmenu-lxqt
Summary:       Library providing a way to implement DBusMenu protocol for LXQt
Version:       0.1.0
Release:       1%{?dist}
License:       LGPL-2.0-or-later
URL:           https://lxqt-project.org/
Source0:       https://github.com/lxqt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6DBus)

%description
%{summary}.

%package devel
Summary:        Qt - development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files used for developing and building software that uses %{name}.

%prep
%autosetup

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license COPYING
%{_libdir}/libdbusmenu-lxqt.so.0
%{_libdir}/libdbusmenu-lxqt.so.%{version}

%files devel
%{_libdir}/cmake/dbusmenu-lxqt
%{_includedir}/dbusmenu-lxqt
%{_libdir}/libdbusmenu-lxqt.so
%{_libdir}/pkgconfig/dbusmenu-lxqt.pc

%changelog
* Thu Apr 18 2024 Steve Cossette <farchord@gmail.com> - 0.1.0-1
- 0.1.0
