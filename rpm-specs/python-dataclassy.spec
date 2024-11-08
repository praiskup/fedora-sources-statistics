%global pypi_name dataclassy
%global common_description %{expand:
An enhanced, tiny reimplementation of data classes in Python - an alternative
to the built-in dataclasses module that avoids many of its common pitfalls.
dataclassy is designed to be more flexible, less verbose, and more powerful
than dataclasses, while retaining a familiar interface.}

Name:          python-%{pypi_name}
Version:       1.0.1
Release:       %autorelease
BuildArch:     noarch
Summary:       An enhanced, tiny reimplementation of dataclasses
License:       MPL-2.0
URL:           https://github.com/biqqles/%{pypi_name}
VCS:           git:%{url}.git
Source0:       %{pypi_source %{pypi_name}}
# FIXME should go into PyPi package
Source1:       python-dataclassy-tests.py
BuildRequires: python3-devel
BuildRequires: python3-mypy


%description %{common_description}

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# FIXME should go into PyPi package
install -D -p -m 0644 %{SOURCE1} tests.py

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
%pyproject_check_import
%python3 tests.py

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE.md
%doc README.md

%changelog
%autochangelog
