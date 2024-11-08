%global pypi_name ipfshttpclient
%global prerelease a2

Name:          python-%{pypi_name}
Version:       0.8.0
Release:       %autorelease -p -s %{prerelease}
BuildArch:     noarch
Summary:       A Python client library for the IPFS API
License:       MIT
URL:           https://github.com/ipfs-shipyard/py-ipfs-http-client
VCS:           git:%{url}.git
Source0:       %{pypi_source %{pypi_name} %{version}%{prerelease}}
# Fedora-specific. Fedora ships a higher but still compatible versions of a
# build dependencies.
Patch1:        python-ipfshttpclient-0001-Relax-dependencies.patch
# Likewise. Our pytest is a very recent.
Patch2:        python-ipfshttpclient-0002-Adjust-test-for-Pytest-7.patch
# Some tests requires a working IPFS node which we don't have in Fedora. Even
# if we have one it will require internet access to operate properly which is
# not available while building.
Patch3:        python-ipfshttpclient-0003-Workaround-until-we-test-with-available-IPFS-node.patch
BuildRequires: python3-devel
BuildRequires: python3-httpcore
BuildRequires: python3-httpx
BuildRequires: python3-pytest
BuildRequires: python3-pytest-cid
BuildRequires: python3-pytest-cov
BuildRequires: python3-pytest-dependency

%description
%{summary}.

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name}
%{summary}.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}%{prerelease}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md RELEASE.md
%license LICENSE

%changelog
%autochangelog
