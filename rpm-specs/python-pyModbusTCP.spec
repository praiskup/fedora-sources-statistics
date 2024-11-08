# Created by pyp2rpm-3.2.2
%global pypi_name pyModbusTCP

Name:           python-%{pypi_name}
Version:        0.3.0
Release:        %autorelease
Summary:        A simple Modbus/TCP library for Python

License:        MIT
URL:            https://github.com/sourceperl/pyModbusTCP
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel

%description
pyModbusTCP A simple Modbus/TCP client library for Python.
Since version 0.1.0, a server is also available for test 
purpose only (don't use in project). pyModbusTCP is pure Python 
code without any extension or external module dependency.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
pyModbusTCP A simple Modbus/TCP client library for Python.
Since version 0.1.0, a server is also available for test 
purpose only (don't use in project). pyModbusTCP is pure Python 
code without any extension or external module dependency.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pyModbusTCP

%check
%py3_check_import pyModbusTCP

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
