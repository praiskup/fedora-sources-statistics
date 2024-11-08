%global pypi_name path-and-address

Name:           python-%{pypi_name}
Version:        2.0.1
Release:        %{autorelease}
Summary:        Functions for server command-line arguments used by humans

%global forgeurl https://github.com/joeyespo/path-and-address
%forgemeta

License:        MIT
URL:            %forgeurl
Source:         %forgesource
# Apply patch making the tests actually useful.
# PytestAssertRewriteWarning: assertion is always true, perhaps remove parentheses?
# https://github.com/joeyespo/path-and-address/pull/4
Patch:          %{forgeurl}/pull/4.patch
# Accept `:0` and `0.0.0.0` as valid
# https://github.com/joeyespo/path-and-address/pull/5
Patch:          %{forgeurl}/pull/5.patch

BuildArch:      noarch
BuildRequires:  python3-devel
# For tests
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Path-and-address resolves ambiguities for command-line interface
applications with the following pattern:

  $ your_app [<path>] [<address>]

The library applies the principal of least surprise to command-line
interfaces.}

%description %_description


%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %_description


%prep
%forgeautosetup -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l path_and_address


%check
%pytest -v
# Run import test in addition to the handful of unit tests
%pyproject_check_import


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc CHANGES.md README.md


%changelog
%autochangelog
