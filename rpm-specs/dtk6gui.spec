Name:           dtk6gui
Version:        6.0.19
Release:        %autorelease
Summary:        Deepin Toolkit, gui module for DDE look and feel
License:        LGPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dtk6gui
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# https://github.com/linuxdeepin/dtkgui/pull/259
Patch0:         dtk6gui-add-qt6.8-support.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build

BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6ToolsTools)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}

BuildRequires:  cmake(Dtk6Core)
BuildRequires:  cmake(DtkBuildHelper)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  freeimage-devel
BuildRequires:  pkgconfig(libraw)

%description
Deepin Tool Kit (DtkGui) is the development graphical user interface of all
C++/Qt Developer work on Deepin.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1

%build
%cmake -GNinja -DDTK_VERSION=%{version}
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libdtk6gui.so.6*
%{_libexecdir}/dtk6/DGui/

%files devel
%{_libdir}/libdtk6gui.so
%{_includedir}/dtk6/DGui/
%{_libdir}/cmake/Dtk6Gui/
%{_libdir}/pkgconfig/dtk6gui.pc
%{_qt6_archdatadir}/mkspecs/modules/*.pri

%changelog
%autochangelog
