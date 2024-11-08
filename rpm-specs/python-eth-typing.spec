%global pypi_name eth_typing

Name:          python-eth-typing
Version:       5.0.0
Release:       %autorelease
BuildArch:     noarch
Summary:       Python types for type hinting commonly used Ethereum types
License:       MIT
URL:           https://github.com/ethereum/eth-typing
VCS:           git:%{url}.git
Source0:       %{pypi_source %pypi_name}
BuildRequires: python3-devel
BuildRequires: python3-pytest

%description
%{summary}.

%package -n python3-eth-typing
Summary: %{summary}

%description -n python3-eth-typing
%{summary}.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
%pyproject_check_import
%pytest

%files -n python3-eth-typing -f %{pyproject_files}
%doc README.md

%changelog
%autochangelog
