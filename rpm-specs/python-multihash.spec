%global pypi_name multihash

Name:          python-%{pypi_name}
Version:       2.0.1
Release:       %autorelease
BuildArch:     noarch
Summary:       Multihash implementation in Python
License:       MIT
URL:           https://github.com/multiformats/py-%{pypi_name}
VCS:           git:%{url}.git
Source0:       %{pypi_source py-multihash}
BuildRequires: python3-devel
BuildRequires: python3-pytest

%description
%{summary}.

%package -n python3-%{pypi_name}
Summary: %{summary}.

%description -n python3-%{pypi_name}
%{summary}.

%prep
%autosetup -p1 -n py-%{pypi_name}-%{version}

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
%doc AUTHORS.rst HISTORY.rst README.rst

%changelog
%autochangelog
