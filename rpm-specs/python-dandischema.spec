%global pypi_name dandischema

# Allow skipping tests
%bcond tests 1
 
Name:           python-%{pypi_name}
Version:        0.10.3
Release:        %{autorelease}
Summary:        Python library for maintaining and managing DANDI metadata schemata
License:        Apache-2.0

# ref was set to v0.10.2 by forge causing download to fail
# so manually set it
%global ref %{version} 
%global forgeurl https://github.com/dandi/dandi-schema
%forgemeta
URL:            %forgeurl
Source:         %forgesource

# Patch for source tarball to exlude tests from wheel
Patch:          %{forgeurl}/pull/249.patch

BuildArch:      noarch
BuildRequires:  python3-devel

# For setuptools_scm
BuildRequires:  git-core

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-rerunfailures)
%endif

%global _description %{expand:
Every Dandiset and associated asset has a metadata object that 
can be retrieved using the DANDI API. This library helps create 
and validate DANDI schema-compliant metadata for Dandisets and assets.}
 
%description %_description
 
%package -n python3-%{pypi_name}
Summary:        %{summary}
 
%description -n python3-%{pypi_name} %_description

%prep

%forgeautosetup -p1 -S git 

# Remove test cov checkers from tox 'test' env
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -i 's/--cov=dandischema //' tox.ini

git add --all
git commit -m '[Packaging]: Downstream changes for %{version}'

# Make sure this is the last step in prep
# to avoid PYTHON_PROVIDED_VERSION_NORMALIZES_TO_ZERO___SEE_STDERR
git tag %{version}

%generate_buildrequires
%pyproject_buildrequires
 
 
%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}
 
 
%check
%if %{with tests}
# Exclude tests which need network
export DANDI_TESTS_NONETWORK=1
%pytest -v
%endif
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md CHANGELOG.md
 
 
%changelog
%autochangelog
