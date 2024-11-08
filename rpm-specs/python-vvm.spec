%global pypi_name vvm
%global common_description %{expand:
Python wrapper and version management tool for the Vyper compiler.}

Name:          python-%{pypi_name}
Version:       0.3.1
Release:       %autorelease
BuildArch:     noarch
Summary:       Vyper version manager
License:       MIT
URL:           https://github.com/vyperlang/vvm
VCS:           git:%{url}.git
# FIXME PyPi package missing ./tests/conftest.py
# Source0:       %{pypi_source %{pypi_name}}
Source0:       %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-pytest-cov

%description %{common_description}

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
%pyproject_check_import
# FIXME unfortunately tests requires internet access which we currently do not
# have in Koji
#%%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md

%changelog
%autochangelog
