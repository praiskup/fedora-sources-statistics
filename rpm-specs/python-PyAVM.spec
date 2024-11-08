%global srcname PyAVM

Name: python-%{srcname}
Version: 0.9.6
Release: %autorelease
Summary: Python package to handle Astronomy Visualization Metadata
License: MIT AND BSD-3-Clause

URL: https://astrofrog.github.io/pyavm/
Source0: %{pypi_source}

BuildArch: noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

#BuildRequires: python3dist(astropy)
#BuildRequires: python3dist(pillow)

Requires: python3dist(astropy)
Requires: python3dist(pillow)

%global _description %{expand:
PyAVM is a Python module to represent, read, and write metadata 
following the *Astronomy Visualization Metadata* (AVM) standard.}     

%description %_description

%package -n python3-%{srcname}
Summary: %{summary}

%description -n python3-%{srcname}
%_description

%prep
%autosetup -n %{srcname}-%{version} 

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files pyavm

%check
%{tox}

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst 

%changelog
%autochangelog
