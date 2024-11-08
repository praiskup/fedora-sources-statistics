%global pypi_name baseconv

Name:          python-%{pypi_name}
Version:       1.2.2
Release:       %autorelease
BuildArch:     noarch
Summary:       A basic baseconv implementation in python
License:       PSF-2.0
URL:           https://github.com/semente/%{name}
VCS:           git:%{url}.git
Source0:       %{pypi_source %{name}}
BuildRequires: python3-devel

%description
%{summary}.

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name}
%{summary}.

%prep
%autosetup -p1 -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
%pyproject_check_import
# FIXME - no tests

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
