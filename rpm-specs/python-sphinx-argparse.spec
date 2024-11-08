%global upname sphinx-argparse
%global srcname sphinx_argparse

Name: python-%{upname}
Version: 0.5.2
Release: %autorelease
Summary: Sphinx extension that automatically documents argparse commands and options
BuildArch: noarch

License: MIT
Url: https://github.com/ashb/sphinx-argparse
Source: %{pypi_source %{srcname}}

BuildRequires:  python3-devel
BuildRequires: %{py3_dist pytest}
BuildRequires: %{py3_dist lxml}

%description
Sphinx extension that automatically documents argparse commands and options

%package -n python3-%{upname}
Summary: %{summary}

%description -n python3-%{upname}
Sphinx extension that automatically documents argparse commands and options

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires 

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files sphinxarg

%check
%pytest

%files -n python3-%{upname} -f %{pyproject_files}
%license LICENCE.rst
%doc README.rst

%changelog
%autochangelog
