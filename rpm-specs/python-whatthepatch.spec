%global pypi_name whatthepatch

Name:           python-%{pypi_name}
Version:        1.0.6
Release:        %autorelease
Summary:        A patch parsing and application library

# SPDX
License:        MIT
URL:            https://github.com/cscorley/whatthepatch
Source:         %{pypi_source %{pypi_name}}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%global _description %{expand:
What The Patch!? is a library for both parsing and applying
patch files.
}

%description %_description

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}
/usr/bin/sed -i 's|\r$||' README.rst

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files -l %{pypi_name}

%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
