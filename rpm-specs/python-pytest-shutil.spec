%global srcname pytest-shutil
%global sum A goodie-bag of unix shell and environment tools for py.test

Name:           python-%{srcname}
Version:        1.8.0
Release:        %autorelease
Summary:        %{sum}

License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source:         %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel

%description
This library is a goodie-bag of Unix shell and 
environment management tools for automated tests.

%package -n python3-%{srcname}
Summary:        %{sum}

%description -n python3-%{srcname}
This library is a goodie-bag of Unix shell and 
environment management tools for automated tests.

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pytest_shutil

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md CHANGES.md

%changelog
%autochangelog
