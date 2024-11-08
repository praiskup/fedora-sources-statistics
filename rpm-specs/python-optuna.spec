# Created by pyp2rpm-3.3.10
%global pypi_name optuna
%global pypi_version 3.6.1

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        2%{?dist}
Summary:        A hyperparameter optimization framework

License:        MIT AND BSD-3-Clause AND SunPro
URL:            https://optuna.org/
Source0:        %{pypi_source}

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

BuildArch:      noarch

%description
Optuna is an automatic hyperparameter optimization software framework,
particularly designed for machine learning. It features an imperative,
define-by-run style user API. Thanks to our define-by-run API, the
code written with Optuna enjoys high modularity, and the user of
Optuna can dynamically construct the search spaces for the hyperparameters.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Optuna is an automatic hyperparameter optimization software framework,
particularly designed for machine learning. It features an imperative,
define-by-run style user API. Thanks to our define-by-run API, the
code written with Optuna enjoys high modularity, and the user of
Optuna can dynamically construct the search spaces for the hyperparameters.

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install

# Tests require fakeredis, not in Fedora

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/optuna
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/

%changelog
* Thu Apr 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.6.1-2
- Fix license tags

* Tue Apr 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.6.1-1
- Initial package.
