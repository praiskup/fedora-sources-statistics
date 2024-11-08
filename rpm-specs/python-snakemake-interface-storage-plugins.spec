# Work around a circular dependency on snakemake and on
# python-snakemake-storage-plugin-http.
%bcond bootstrap 0
# We can’t run tests that access the network in koji, but this build
# conditional allows us to try them in local mock builds for added confidence:
#   fedpkg mockbuild --enable-network --with network_tests
%bcond network_tests 0

Name:           python-snakemake-interface-storage-plugins
Version:        3.3.0
Release:        %autorelease
Summary:        Stable interface for interactions between Snakemake and its storage plugins

# SPDX
License:        MIT
URL:            https://github.com/snakemake/snakemake-interface-storage-plugins
# We use the GitHub archive instead of the PyPI sdist to get CHANGELOG.md and
# the tests.
Source:         %{url}/archive/v%{version}/snakemake-interface-storage-plugins-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
%if %{without bootstrap}
# See: [tool.poetry.dev-dependencies] in pyproject.toml
BuildRequires:  %{py3_dist pytest}
BuildRequires:  snakemake >= 8
BuildRequires:  %{py3_dist snakemake-storage-plugin-http}
%endif

%global common_description %{expand:
This package provides a stable interface for interactions between Snakemake and
its storage plugins.}

%description %{common_description}


%package -n python3-snakemake-interface-storage-plugins
Summary:        %{summary}

%description -n python3-snakemake-interface-storage-plugins %{common_description}


%prep
%autosetup -n snakemake-interface-storage-plugins-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files snakemake_interface_storage_plugins


%check
%if %{without bootstrap}
# Just in case the tests are not very thorough:
%pyproject_check_import

%if %{without network_tests}
# The following tests require network access:
k="${k-}${k+ and }not (TestTestStorageBase and test_storage)"
k="${k-}${k+ and }not (TestTestStorageBase and test_storage_not_existing)"
k="${k-}${k+ and }not (TestTestStorageBase and test_inventory)"
%endif

%pytest -k "${k-}" -v tests/tests.py
%else
# Some things can’t be imported because we don’t have snakemake during
# bootstrapping.
%pyproject_check_import -e '*.registry*' -e '*.storage_object' -e '*.tests'
%endif


%files -n python3-snakemake-interface-storage-plugins -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md
%doc README.md


%changelog
%autochangelog
