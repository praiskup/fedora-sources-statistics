# Note that we *do* need mypy for some of the tests; it is not just a
# “typechecking linter.” However, we can optionally skip those tests.
%bcond mypy 1

Name:           python-typeguard
Version:        4.3.0
Release:        %autorelease
Summary:        Run-time type checker for Python

# SPDX
License:        MIT
URL:            https://github.com/agronholm/typeguard
Source:         %{pypi_source typeguard}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  tomcli

%global common_description %{expand:
This library provides run-time type checking for functions defined with PEP 484
argument (and return) type annotations.}

%description %{common_description}


%package -n python3-typeguard
Summary:        %{summary}

# Removed for F41:
Obsoletes:      python-typeguard-doc < 4.2.1-2

%description -n python3-typeguard %{common_description}


%prep
%autosetup -n typeguard-%{version}

# Downstream-only: do not treat warnings in tests as errors
#
# This makes sense for upstream development and CI, but is too strict for
# distribution packaging.
tomcli set pyproject.toml lists delitem \
    'tool.pytest.ini_options.filterwarnings' error

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
tomcli set pyproject.toml lists delitem --type regex \
    'project.optional-dependencies.test' 'coverage\b.*'

%if 0%{?el10}
# Loosen the typing_extensions dependency version bound. Upstream needed 4.10.0
# for Python 3.13 support. EPEL10 has only 4.9.0, but it also has Python 3.12,
# so this should be OK.
tomcli set pyproject.toml lists replace --type regex project.dependencies \
    'typing_extensions >= 4\..*' 'typing_extensions >= 4.9.0'
%endif
%if %{without mypy}
tomcli set pyproject.toml lists delitem --type regex \
    project.optional-dependencies.test 'mypy\b.*'
%endif


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_buildrequires -x test


%build
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_wheel


%install
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_install
%pyproject_save_files -l typeguard


%check
%if %{without mypy}
k="${k-}${k+ and }not test_negative"
k="${k-}${k+ and }not test_positive"
%endif

%pytest -k "${k-}" -v -rs


%files -n python3-typeguard -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
