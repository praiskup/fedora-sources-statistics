%global pypi_name zarr-checksum
 
Name:           python-%{pypi_name}
Version:        0.4.2
Release:        %{autorelease}
Summary:        Algorithms for calculating a zarr checksum against local or cloud storage
License:        Apache-2.0

# ref was setting to 0.4.2 by forge causing download to fail.
# so manually set it
%global ref v%{version} 
%global forgeurl https://github.com/dandi/zarr_checksum
%forgemeta
URL:            %forgeurl
Source:         %forgesource
 
BuildArch:      noarch
BuildRequires:  python3-devel
# Test dependencies:
BuildRequires:  python3dist(pytest)

# Allow users to install this rpm as 'zarrsum'
Provides: zarrsum = %{version}-%{release}

%global _description %{expand:
Algorithms for calculating a zarr checksum against local or cloud storage.}
 
%description %_description
 
%package -n python3-%{pypi_name}
Summary:        %{summary}
 
%description -n python3-%{pypi_name} %_description
 
 
%prep
%forgeautosetup
 
 
%generate_buildrequires
%pyproject_buildrequires -e test
 
 
%build
%pyproject_wheel
 
%install
%pyproject_install
%pyproject_save_files -L zarr_checksum
 
 
%check
%tox -e test
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}
%{_bindir}/zarrsum
%doc README.md NOTICE
%license LICENSE
 
 
%changelog
%autochangelog
