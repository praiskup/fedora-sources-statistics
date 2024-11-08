%global pypi_name multiaddr

Name:          python-%{pypi_name}
Version:       0.0.9
Release:       %autorelease
BuildArch:     noarch
Summary:       Multiaddr implementation in Python
License:       MIT
URL:           https://github.com/multiformats/py-multiaddr
Source0:       %{pypi_source %{pypi_name}}
BuildRequires: python3-devel
BuildRequires: python3-idna
BuildRequires: python3-pytest

%description
%{summary}.

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name}
%{summary}.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

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
%doc AUTHORS HISTORY.rst README.rst

%changelog
%autochangelog
