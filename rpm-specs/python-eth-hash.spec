%global pypi_name eth-hash
%global common_description %{expand:
The Ethereum hashing function, keccak256, sometimes (erroneously) called sha256
or sha3.}

Name:          python-%{pypi_name}
Version:       0.7.0
Release:       %autorelease
BuildArch:     noarch
Summary:       The Ethereum hashing function
License:       MIT
URL:           https://github.com/ethereum/eth-hash
VCS:           git:%{url}.git
Source0:       %{pypi_source %pypi_name}
# Fedora-specific. Cryptodome shipped in Fedora is not drop-in replacement for
# pycrypto. We have to adjust.
Patch1:        python-eth_hash-0001-Fedora-use-cryptodome-explicitly.patch
# Fedora-secific. We don't have pysha3
Patch2:        python-eth_hash-0002-Remove-pysha3.patch
BuildRequires: python3-devel
BuildRequires: python3-pycryptodomex
BuildRequires: python3-pytest

%description  %{common_description}

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l eth_hash

%check
%pyproject_check_import
%pytest ./tests/core/ ./tests/backends/pycryptodome

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md

%changelog
%autochangelog
