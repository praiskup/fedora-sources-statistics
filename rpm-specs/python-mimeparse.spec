Name:           python-mimeparse
Version:        2.0.0
Release:        %autorelease
Summary:        Python module for parsing mime-type names
License:        MIT
URL:            https://github.com/falconry/python-mimeparse
Source:         %{pypi_source python_mimeparse}
BuildArch:      noarch

%global common_description %{expand:
This module provides basic functions for handling mime-types.  It can handle
matching mime-types against a list of media-ranges.}


%description %{common_description}


%package -n python3-mimeparse
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest


%description -n python3-mimeparse %{common_description}


%prep
%autosetup -p 1 -n python_mimeparse-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l mimeparse


%check
%pytest


%files -n python3-mimeparse -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
