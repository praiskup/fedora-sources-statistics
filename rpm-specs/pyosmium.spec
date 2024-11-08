%global libosmium_version 2.20.0
%global pybind_version 2.11.1

Name:           pyosmium
Version:        4.0.2
Release:        %autorelease
Summary:        Python bindings for libosmium

License:        BSD-2-Clause
URL:            https://osmcode.org/pyosmium/
Source0:        https://github.com/osmcode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# Disable stripping
Patch0:         pyosmium-no-strip.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake make
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  argparse-manpage
BuildRequires:  pybind11-devel >= %{pybind_version}
BuildRequires:  boost-devel
BuildRequires:  libosmium-devel >= %{libosmium_version}
BuildRequires:  libosmium-static >= %{libosmium_version}

%description
Provides Python bindings for the Libosmium C++ library, a library
for working with OpenStreetMap data in a fast and flexible manner.


%package -n python3-osmium
Summary:        %{summary}

%description -n python3-osmium
Provides Python bindings for the Libosmium C++ library, a library
for working with OpenStreetMap data in a fast and flexible manner.


%prep
%autosetup -p1


%generate_buildrequires
%pyproject_buildrequires -x tests


%build
%pyproject_wheel
PYTHONPATH=$PWD/build/lib.%{python3_platform}-cpython-%{python3_version_nodots} %make_build -C docs man


%install
%pyproject_install
%pyproject_save_files osmium
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m644 docs/man/*.1 %{buildroot}%{_mandir}/man1


%check
%pytest


%files -n python3-osmium -f %{pyproject_files}
%doc README.md README.rst CHANGELOG.md docs/*.md docs/reference docs/user_manual
%license LICENSE.TXT
%{_bindir}/*
%{_mandir}/man1/*


%changelog
%autochangelog
