%global module_name cangjie
%global forgeurl https://gitlab.freedesktop.org/cangjie/pycangjie
%global archiveext tar.bz2

Name:             python3-%{module_name}
Summary:          Python bindings to libcangjie
Version:          1.5.0
Release:          %{autorelease}
%forgemeta
License:          LGPL-3.0-only
URL:              https://gitlab.freedesktop.org/cangjie/pycangjie
Source0:          %{forgesource}

%forgemeta

BuildRequires:    gcc
BuildRequires:    meson
BuildRequires:    python3dist(cython)
BuildRequires:    python3-devel
BuildRequires:    libcangjie-devel >= 1.4.0


%description
Python bindings to libcangjie, the library implementing Cangjie and Quick
input methods.


%prep
%autosetup -n pycangjie-%{version}


%build
%meson
%meson_build


%install
%meson_install

find %{buildroot} -name '*.la' -exec rm -f '{}' \;


%check
export CANGJIE_DB=/usr/share/libcangjie/cangjie.db
%meson_test


%files
%license COPYING
%doc README.md docs/*.md
%{python3_sitearch}/%{module_name}


%changelog
%autochangelog
