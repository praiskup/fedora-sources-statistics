Name:           python-editables
Version:        0.5
Release:        %autorelease
Summary:        Editable installations

# SPDX
License:        MIT
URL:            https://github.com/pfmoore/editables
# PyPI source distributions lack tests; use the GitHub archive
Source:         %{url}/archive/%{version}/editables-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

# Most of the dependencies, and all of the pytest options, in tox.ini are for
# coverage analysis and for installation with pip/virtualenv. Rather than
# working around all of these, it is simpler not to use tox for dependency
# generation or testing.
BuildRequires:  python3dist(pytest)

%global common_description %{expand:
A Python library for creating “editable wheels”

This library supports the building of wheels which, when installed, will expose
packages in a local directory on sys.path in “editable mode”. In other words,
changes to the package source will be reflected in the package visible to
Python, without needing a reinstall.}

%description %{common_description}


%package -n python3-editables
Summary:        %{summary}

# Dropped in F41
Obsoletes:      python-editables-doc < 0.5-5

%description -n python3-editables %{common_description}


%prep
%autosetup -n editables-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files editables


%check
%pytest


%files -n python3-editables -f %{pyproject_files}
%license LICENSE.txt
%doc CHANGELOG.md
%doc README.md


%changelog
%autochangelog
