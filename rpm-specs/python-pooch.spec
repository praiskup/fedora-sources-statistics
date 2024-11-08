# Quite a few tests require network. To run them locally use
# `fedpkg mockbuild --enable-network --with network`
%bcond network 0

Name:           python-pooch
Version:        1.8.2
Release:        %autorelease
Summary:        A friend to fetch your data files

%global forgeurl https://github.com/fatiando/pooch
%forgemeta

License:        BSD-3-Clause
URL:            https://www.fatiando.org/pooch
Source:         %forgesource
# Include `tests/data/` in wheel
# https://github.com/fatiando/pooch/pull/421
Patch:          https://github.com/fatiando/pooch/pull/421.patch
# Exclude `doc/` from wheel
# https://github.com/fatiando/pooch/pull/423
Patch:          https://github.com/fatiando/pooch/pull/423.patch

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
Pooch manages your Python library's sample data files: 
it automatically downloads and stores them in a local directory, 
with support for versioning and corruption checks.}

%description %_description


%package -n python3-pooch
Summary:        %{summary}

%description -n python3-pooch %_description


%prep
%forgeautosetup -p1

# Remove coverage dependencies
sed -i \
  -e '/cov/ d' \
  env/requirements-test.txt


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires -x progress,xxhash%{?network:,sftp} env/requirements-test.txt


%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l pooch


%check
%pytest -v ${k+-k }"${k-}" %{?!network:-m 'not network'}


%files -n python3-pooch -f %{pyproject_files}
%doc README.md CITATION.* AUTHORS.md


%changelog
%autochangelog
