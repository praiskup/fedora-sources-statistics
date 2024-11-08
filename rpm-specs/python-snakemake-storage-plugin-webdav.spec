Name:           python-snakemake-storage-plugin-webdav
Version:        0.1.1
Release:        %autorelease
Summary:        Snakemake storage plugin for webdav

# SPDX
License:        MIT
URL:            https://github.com/snakemake/snakemake-storage-plugin-webdav
# We use the GitHub archive instead of the PyPI sdist to get CHANGELOG.md and
# the tests.
Source:         %{url}/archive/v%{version}/snakemake-storage-plugin-webdav-%{version}.tar.gz
# Do not use SemVer-based version bounds for fsspec
# https://github.com/snakemake/snakemake-storage-plugin-webdav/pull/5
Patch:          %{url}/pull/5.patch
# Update webdav4 dependency to 0.10.0
# https://github.com/snakemake/snakemake-storage-plugin-webdav/pull/6
# Rebased to apply on top of 5.patch, above.
Patch:          0001-Update-webdav4-dependency-to-0.10.0.patch

BuildArch:      noarch

BuildRequires:  python3-devel
# See: [tool.poetry.dev-dependencies] in pyproject.toml
BuildRequires:  %{py3_dist pytest}
BuildRequires:  snakemake >= 8

%global common_description %{expand:
A Snakemake storage plugin for handling input and output via webdav.}

%description %{common_description}


%package -n python3-snakemake-storage-plugin-webdav
Summary:        %{summary}

%description -n python3-snakemake-storage-plugin-webdav %{common_description}


%prep
%autosetup -n snakemake-storage-plugin-webdav-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files snakemake_storage_plugin_webdav


%check
# Just in case the tests are not very thorough:
%pyproject_check_import

# The following tests require network access and a webdav test server that
# upstream CI sets up with docker, which will of course not be possible here:
k="${k-}${k+ and }not (TestStorage and test_storage)"
k="${k-}${k+ and }not (TestStorage and test_storage_not_existing)"

%pytest -v -k "${k-}" tests/tests.py


%files -n python3-snakemake-storage-plugin-webdav -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md
%doc README.md


%changelog
%autochangelog
