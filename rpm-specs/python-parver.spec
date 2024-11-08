%global pypi_name parver
Name:           python-%{pypi_name}
Version:        0.5
Release:        %autorelease
Summary:        Parse and manipulate version numbers

License:        MIT
URL:            https://github.com/RazerM/parver
Source0:        %pypi_source
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
Parver allows parsing and manipulation of PEP 440 version numbers.


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Parver allows parsing and manipulation of PEP 440 version numbers.


%prep
%autosetup -n %{pypi_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test -x doctest


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files parver

%check
%pytest -v


%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
%autochangelog
