%global repo dde-network-core
%global __provides_exclude_from ^%{_prefix}/lib/*/modules/.*\\.so$

Name:           deepin-network-core
Version:        2.0.32
Release:        %autorelease
Summary:        DDE network library and plugins
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-network-core
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5Help)

BuildRequires:  cmake(KF5NetworkManagerQt)

BuildRequires:  cmake(DtkWidget)
BuildRequires:  cmake(DtkCore)
BuildRequires:  cmake(DdeControlCenter)
BuildRequires:  cmake(DdeDock)
BuildRequires:  cmake(DdeSessionShell)
BuildRequires:  cmake(GTest)

BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gsettings-qt)

Requires:       %{name}-lib%{?_isa} = %{version}-%{release}
# provides %%{_var}/lib/polkit-1/localauthority/10-vendor.d
Requires:       polkit-pkla-compat

%description
This package provides %{summary}.

%package        lib
Summary:        Shared library files for %{name}

%description    lib
This package contains shared library files for %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-lib%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1 -n %{repo}-%{version}

%build
%cmake -GNinja
%cmake_build

%install
%cmake_install
%find_lang dcc-network-plugin --with-qt
%find_lang dss-network-plugin --with-qt
rm %{buildroot}%{_datadir}/dde-control-center/translations/dcc-network-plugin.qm
rm %{buildroot}%{_datadir}/dss-network-plugin/translations/dss-network-plugin.qm

%files -f dcc-network-plugin.lang -f dss-network-plugin.lang
%dir %{_prefix}/lib/dde-session-shell
%dir %{_prefix}/lib/dde-session-shell/modules
%{_prefix}/lib/dde-session-shell/modules/libdss-network-plugin.so
%dir %{_libdir}/dde-control-center
%dir %{_libdir}/dde-control-center/modules
%{_libdir}/dde-control-center/modules/libdcc-network-plugin.so
%{_datadir}/polkit-1/rules.d/50-dss-network-plugin.rules
%{_datadir}/dsg/

%files lib
%{_libdir}/libdde-network-core.so.2*

%files devel
%{_includedir}/libddenetworkcore/
%{_libdir}/libdde-network-core.so
%{_libdir}/pkgconfig/%{repo}.pc

%changelog
%autochangelog
