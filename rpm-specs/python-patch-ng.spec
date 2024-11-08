%global pypi_name patch-ng

%global _description %{expand:
Fork of the original python-patch library to parse
and apply unified diffs.}

Name: python-%{pypi_name}
Version: 1.18.0
Release: %autorelease

License: MIT
Summary: Library to parse and apply unified diffs
URL: https://github.com/conan-io/%{name}
Source0: %{pypi_source %{pypi_name}}
BuildArch: noarch

BuildRequires: python3-devel

%description %_description

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files patch_ng

%check
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
%autochangelog
