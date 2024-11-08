%global pypi_name solcx

Name:          python-%{pypi_name}
Version:       2.0.3
Release:       %autorelease
BuildArch:     noarch
Summary:       Python wrapper and version management tool for the Solidity compiler
License:       MIT
URL:           https://github.com/ApeWorX/py-solc-x
VCS:           git:%{url}.git
Source0:       %{pypi_source py-solc-x}
Patch1:        python-solcx-0001-Ease-version-requirements.patch
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-pytest-cov

%description
%{summary}.

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name}
%{summary}.

%prep
%autosetup -p1 -n py-solc-x-%{version}

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
# have in Koji.
#%%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md

%changelog
%autochangelog
