%global pypi_name pygments-lexer-solidity

Name:          python-%{pypi_name}
Version:       0.7.0
Release:       %autorelease
BuildArch:     noarch
Summary:       Solidity lexer for Pygments
License:       BSD-2-Clause
URL:           https://gitlab.com/veox/%{pypi_name}
VCS:           git:%{url}.git
Source0:       %{pypi_source %{pypi_name}}
BuildRequires: python3-devel

%description
%{summary}.

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name}
%{summary}.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l pygments_lexer_solidity


%check
# FIXME - no tests
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
