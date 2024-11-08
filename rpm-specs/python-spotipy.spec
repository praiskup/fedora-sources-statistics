%global pypi_name spotipy

Name:           python-%{pypi_name}
Version:        2.24.0
Release:        3%{?dist}
Summary:        A light weight Python library for the Spotify Web API
License:        MIT
URL:            https://github.com/plamere/spotipy
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%global _description \
A light weight Python library for the Spotify Web API


%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  python3-docutils



%description -n python3-spotipy %{_description}

%package -n python3-spotipy-doc
Summary:        Documentation for python3-spotipy

%description -n python3-spotipy-doc
Documentation for python3-spotipy



%prep
%autosetup -n %{pypi_name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel

PYTHONPATH=$PWD/build/lib
mkdir html
sphinx-build -b html docs html
rm -rf html/{.buildinfo,.doctrees}

%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%check
%pyproject_check_import
# full tests can not be run without network access

%files -n python3-spotipy -f %pyproject_files
%license LICENSE.md
%doc CONTRIBUTING.md TUTORIAL.md FAQ.md CHANGELOG.md

%files -n python3-spotipy-doc
%doc html

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.24.0-2
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

%autochangelog
