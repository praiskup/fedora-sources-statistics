%global         srcname         inkex
%global         forgeurl        https://gitlab.com/inkscape/extensions
Version:        1.3.1
%global         tag             v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        3%{?dist}
Summary:        Python extensions for Inkscape core

License:        GPL-2.0-or-later
URL:            %forgeurl
Source:         %{pypi_source %{srcname}}
Patch:          scour-version.patch
BuildRequires:  python3-devel
# Tests
BuildRequires:  python3dist(pytest)
BuildRequires:  python3-gobject-devel
BuildRequires:  python3-gobject
BuildRequires:  python3-gobject-base
BuildRequires:  python3-gobject-base-noarch
BuildRequires:  gtk3-devel
BuildArch: noarch

%global _description %{expand:
This package supports Inkscape extensions.

It provides
- a simplification layer for SVG manipulation through lxml
- base classes for common types of Inkscape extensions
- simplified testing of those extensions
- a user interface library based on GTK3

At its core, Inkscape extensions take in a file, and output a file.
- For effect extensions, those two files are SVG files.
- For input extensions, the input file may be any arbitrary
  file and the output is an SVG.
- For output extensions, the input is an SVG file while the
  output is an arbitrary file.
- Some extensions (e.g. the extensions manager) don't manipulate files.

This folder also contains the stock Inkscape extensions, i.e. the scripts
that implement some commands that you can use from within Inkscape.
Most of these commands are in the Extensions menu, or in the Open /
Save dialogs.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}
# Remove version limit from lxml
sed -i "s/lxml = .*/lxml = '\*'/" pyproject.toml

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}
# Executable fix
sed -i /env\ python/d %{buildroot}%{python3_sitelib}/inkex/tester/inx.py

%check
%pyproject_check_import


%files -n python3-%{srcname} -f %{pyproject_files}
%doc package-readme.md
%license LICENSE.txt
 
%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.3.1-2
- Rebuilt for Python 3.13

* Wed Apr 10 2024 Benson Muite <benson_muite@emailplus.org> - 1.3.1-1
- Update to latest release on Pypi

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Lumír Balhar <lbalhar@redhat.com> - 1.3.0-3
- Remove version limit from lxml

* Sun Dec 24 2023 Benson Muite <benson_muite@emailplus.org> - 1.3.0-2
- Enable building with Python 3.13

* Fri Sep 08 2023 Benson Muite <benson_muite@emailplus.org> - 1.3.0-1
- Initial package

