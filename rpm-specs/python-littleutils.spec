%global pypi_name littleutils

Name:           python-%{pypi_name}
Version:        0.2.4
Release:        %autorelease
Summary:        Small collection of Python utilities

# SPDX
License:        MIT
URL:            https://github.com/alexmojaki/littleutils
Source:         %{pypi_source %{pypi_name}}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
Small collection of Python utilities.}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}

%changelog
%autochangelog
