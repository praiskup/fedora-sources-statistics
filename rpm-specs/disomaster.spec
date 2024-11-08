Name:           disomaster
Version:        5.0.8
Release:        %autorelease
Summary:        Library to manipulate DISC burning
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/disomaster
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(libisoburn-1)
BuildRequires:  make

%description
DISOMaster provides basic optical drive operation and on-disc filesystem
manipulation.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1
sed -i 's|/lib|/%{_lib}|' libdisomaster/libdisomaster.pro

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%doc README.md
%license LICENSE
%{_libdir}/lib%{name}.so.1*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
