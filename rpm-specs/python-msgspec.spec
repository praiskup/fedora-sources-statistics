%global debug_package %{nil}
%global pypi_name msgspec

Name:           python-%{pypi_name}
Summary:        Fast serialization and validation library
Version:        0.18.6
Source:         https://github.com/jcrist/%{pypi_name}/archive/refs/tags/%{version}/msgspec-%{version}.tar.gz
Release:        %autorelease

License:        BSD-3-Clause
URL:            https://jcristharif.com/msgspec/

# Build Python 3.13 wheels (not free-threaded)
# https://github.com/jcrist/msgspec/pull/711
#
# Fixes Python 3.13 compatibility, RHBZ#2301180. Rebased on 0.18.6, with
# changes to .github/workflows/ci.yml omitted.
Patch:          msgspec-0.18.6-python3.13-pr-711.patch

BuildRequires:  python3-devel
BuildRequires:  python3dist(wheel)
# Adding the pytest dependency manually, as the `tests` extras group also
# includes mypy, pyright, pre-commit and other unpackaged dependencies
BuildRequires:  python3dist(pytest)
BuildRequires:  gcc
ExcludeArch: s390x i686

%generate_buildrequires
%pyproject_buildrequires

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%global _description %{expand:
A fast serialization and validation library, with builtin support for
JSON, MessagePack, YAML, and TOML.}

%description %_description
%description -n python3-%{pypi_name} %_description

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
%autochangelog
