%global pypi_name base58

%global common_description %{expand:
Base58 and Base58Check implementation compatible with what is used by the
bitcoin network.}

Name:          python-%{pypi_name}
Version:       2.1.1
Release:       %autorelease
BuildArch:     noarch
Summary:       Base58 and Base58Check implementation
License:       MIT
URL:           https://github.com/keis/%{pypi_name}
VCS:           git:%{url}.git
Source0:       %{pypi_source %{pypi_name}}
BuildRequires: python3-devel
BuildRequires: python3-hamcrest
BuildRequires: python3-pytest
BuildRequires: python3-pytest-benchmark

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
%pyproject_save_files -l %{pypi_name}

%check
%pyproject_check_import
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%{_bindir}/base58

%changelog
%autochangelog
