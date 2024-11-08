Name:           python-housekeeping
Version:        1.1
Release:        %autorelease
Summary:        Python utilities for helping deprecate and remove code

License:        MIT
URL:            https://pypi.org/project/housekeeping/
Source:         %{pypi_source housekeeping}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)


%global _description %{expand:
Housekeeping is a Python package designed to make it easy for projects to mark
consumed code as deprecated or pending deprecation, with helpful instructions
for consumers using deprecated functionality.}

%description %_description

%package -n     python3-housekeeping
Summary:        %{summary}

%description -n python3-housekeeping %_description


%prep
%autosetup -p1 -n housekeeping-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l housekeeping


%check
%pyproject_check_import
%pytest


%files -n python3-housekeeping -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
