%global forgeurl https://gitlab.freedesktop.org/cangjie/libcangjie
%global archiveext tar.bz2

Name:             libcangjie
Summary:          Cangjie Input Method Library
Version:          1.4.0
Release:          %autorelease
License:          LGPL-3.0-or-later
URL:              http://cangjians.github.io/projects/%{name}
Source0:          https://gitlab.freedesktop.org/cangjie/%{name}/-/archive/v%{version}/%{name}-v%{version}.%{archiveext}

BuildRequires:    gcc
BuildRequires:    sqlite-devel
BuildRequires:    meson

# Split out so it can be noarch
Requires:         %{name}-data = %{version}-%{release}

%description
Library implementing the Cangjie input method.


%package data
Summary:          Database for %{name}
BuildArch:        noarch

%description data
Database for %{name}.


%package devel
Summary:          Development files for %{name}
Requires:         %{name}%{_isa} = %{version}-%{release}
Requires:         sqlite-devel

%description devel
Development files for %{name}.


%prep
%autosetup -n %{name}-v%{version}


%build
%meson
%meson_build


%install
%meson_install

find %{buildroot} -name '*.la' -exec rm -f '{}' \;


%check
%meson_test


%files
%doc AUTHORS COPYING README.md
%{_libdir}/%{name}.so.3*

%files data
%doc data/README.table.md
%{_datadir}/%{name}

%files devel
%doc docs/*.md
%{_bindir}/libcangjie-*
%{_includedir}/cangjie
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/cangjie.pc


%changelog
%autochangelog
