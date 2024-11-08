%bcond tests 1

%global         srcname pycomposefile

Name:           python-%{srcname}
Version:        0.0.32
Release:        %autorelease
Summary:        Structured deserialization of Docker Compose files

License:        MIT
URL:            https://github.com/smurawski/pycomposefile
Source:         %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
Structured deserialization of Docker Compose files}


%description %_description

%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
# Work around an upstream bug with the version number.
# https://github.com/smurawski/pycomposefile/issues/29
export BUILD_TAG='%{version}'
cd src/
%pyproject_buildrequires


%build
export BUILD_TAG='%{version}'
cd src/
%pyproject_wheel


%install
export BUILD_TAG='%{version}'
cd src/
%pyproject_install

# Remove the installed tests.
rm -rf %{buildroot}%{python3_sitelib}/tests

%pyproject_save_files %{srcname}


%check
%pyproject_check_import
#%%pyproject_check_import -e tests.service.test_service_environment

%if %{with tests}
%pytest
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license LICENSE


%changelog
%autochangelog
