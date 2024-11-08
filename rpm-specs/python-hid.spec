%global srcname hid

Name:           python-%{srcname}
Version:        1.0.6
Release:        %autorelease
Summary:        Python ctypes bindings for hidapi

License:        MIT
URL:            https://github.com/apmorton/pyhidapi
Source:         %{pypi_source %{srcname}}

BuildArch:      noarch
BuildRequires:  hidapi
BuildRequires:  python3-devel

%global _description %{expand:
This package provides Python bindings for hidapi using ctypes.}

%description %_description

%package -n     python3-%{srcname}
Summary:        %{summary}
Requires:       hidapi

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{srcname}

%check
%pyproject_check_import

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md

%changelog
%autochangelog
