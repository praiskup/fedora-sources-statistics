# Created by pyp2rpm-3.3.4
%global pypi_name boutdata

Name:           python-%{pypi_name}
Version:        0.2.1
Release:        %autorelease
Summary:        Python package for collecting BOUT++ data

License:        LGPL-3.0-or-later
URL:            http://boutproject.github.io
Source0:        %pypi_source
BuildArch:      noarch

Patch:          0001-pytest-no-cov.patch
Patch:          https://github.com/boutproject/boutdata/commit/2c4500ed56199a55e098d84c399c5a6b3f27544e.patch#./0002-no-gc-collect.patch
Patch:          natsort-version.patch
Patch:          fix-script-dir.patch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
# From setup_requires in setup.py:
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(setuptools-scm[toml]) >= 3.4
# For tests:
BuildRequires:  python3dist(pytest)

%description
Python interface for reading bout++ data files.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Python interface for reading bout++ data files.

%generate_buildrequires
%pyproject_buildrequires -r


%prep
%autosetup -n %{pypi_name}-%{version} -p 1
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%check
# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1997717
export HDF5_USE_FILE_LOCKING=FALSE
# Smoke test for squash
PYTHONPATH=${RPM_BUILD_ROOT}/${PYTHON3_SITELIB}:${PYTHONPATH} ${RPM_BUILD_ROOT}/%{_bindir}/bout-squashoutput --help
# run unit tests
%pytest


%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/bout-squashoutput


%changelog
%{autochangelog}
