%bcond_without tests

Name:           python-platformdirs
Version:        4.2.2
Release:        %autorelease
Summary:        A small Python package for determining appropriate platform-specific dirs
License:        MIT
URL:            https://github.com/platformdirs/platformdirs
Source:         %{pypi_source platformdirs}
BuildArch:      noarch

%global common_description %{expand:
When writing desktop application, finding the right location to store user data
and configuration varies per platform.  Even for single-platform apps, there
may by plenty of nuances in figuring out the right location.  This kind of
thing is what the platformdirs package is for.}


%description %{common_description}


%package -n python3-platformdirs
Summary:        %{summary}
BuildRequires:  python3-devel
# RHBZ#1712140, RHBZ#2076994
BuildRequires:  pyproject-rpm-macros >= 1.2.0


%description -n python3-platformdirs %{common_description}


%prep
%autosetup -n platformdirs-%{version}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -r -i '/^[[:blank:]]*"pytest-cov\b/d' pyproject.toml
sed -r -i '/^[[:blank:]]*"covdefaults\b/d' pyproject.toml


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-x test}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l platformdirs


%check
%if %{with tests}
# Upstream uses tox, but we don’t use it, to avoid a build dependency loop
# platformdirs <- virtualenv <- tox
%pytest
%else
%pyproject_check_import
%endif


%files -n python3-platformdirs -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
