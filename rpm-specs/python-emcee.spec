%bcond_without check

%global srcname emcee

Name: python-%{srcname}
Version: 3.1.6
Release: %autorelease
Summary: The Python ensemble sampling toolkit for affine-invariant MCMC
License: MIT

URL: https://emcee.readthedocs.io/en/stable/
Source0: %{pypi_source}
BuildRequires: python3-devel 
BuildArch: noarch

%global _description %{expand: 
emcee is a stable, well tested Python implementation of the affine-invariant ensemble sampler for Markov chain Monte Carlo (MCMC) proposed by Goodman & Weare (2010). The code is open source and has already been used in several published projects in the Astrophysics literature.}

%description %_description

%package -n python3-%{srcname}
Summary: %{summary}
BuildRequires: %{py3_dist setuptools}
BuildRequires: %{py3_dist setuptools_scm}
%if %{with check}
BuildRequires: %{py3_dist pytest}
BuildRequires: %{py3_dist scipy}
BuildRequires: %{py3_dist h5py}
%endif

%description -n python3-%{srcname}
%_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files emcee

%if %{with check}
%check
# Some tests are failling in ppc64le with longdouble
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_ADDOPTS='-p no:cacheprovider'
pushd %{buildroot}/%{python3_sitelib}
   pytest-%{python3_version} \
%ifarch ppc64le
   --deselect "emcee/tests/integration/test_longdouble.py::test_longdouble_actually_needed[TempHDFBackend]" \
   --deselect "emcee/tests/unit/test_backends.py::test_longdouble_preserved[TempHDFBackend]" \
   --deselect "emcee/tests/unit/test_backends.py::test_hdf5_dtypes" \
%endif
   emcee
popd
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%doc AUTHORS.rst HISTORY.rst README.rst 

%changelog
%autochangelog
