Name:           python-snakemake-storage-plugin-xrootd
Version:        0.1.4
Release:        %autorelease
Summary:        Snakemake storage plugin for xrootd storage

# SPDX
License:        MIT
URL:            https://github.com/snakemake/snakemake-storage-plugin-xrootd
# We use the GitHub archive instead of the PyPI sdist to get CHANGELOG.md and
# the tests.
Source:         %{url}/archive/v%{version}/snakemake-storage-plugin-xrootd-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
# See: [tool.poetry.dev-dependencies] in pyproject.toml
BuildRequires:  %{py3_dist pytest}
BuildRequires:  snakemake >= 8

%global common_description %{expand:
A Snakemake storage plugin for handling input and output via XRootD.}

%description %{common_description}


%package -n python3-snakemake-storage-plugin-xrootd
Summary:        %{summary}

%description -n python3-snakemake-storage-plugin-xrootd %{common_description}


%prep
%autosetup -n snakemake-storage-plugin-xrootd-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files snakemake_storage_plugin_xrootd


%check
# Just in case the tests are not very thorough:
%pyproject_check_import

# The following test requires a running XRootD server; this may or may not be
# possible to arrange, but would be tedious and complex at best.
k="${k-}${k+ and }not (TestStorage and test_storage)"

%pytest -v -k "${k-}" tests/tests.py


%files -n python3-snakemake-storage-plugin-xrootd -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md
%doc README.md


%changelog
%autochangelog
