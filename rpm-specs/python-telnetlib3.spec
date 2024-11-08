Name:           python-telnetlib3
Version:        2.0.4
Release:        %autorelease
Summary:        Python 3 asyncio Telnet server and client Protocol library

License:        ISC
URL:            http://telnetlib3.rtfd.org/
Source:         %{pypi_source telnetlib3}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
telnetlib3 is a Telnet Client and Server library for Python.}

%description %_description

%package -n     python3-telnetlib3
Summary:        %{summary}

%description -n python3-telnetlib3 %_description

%prep
%autosetup -p1 -n telnetlib3-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files telnetlib3

%check
%tox

%files -n python3-telnetlib3 -f %{pyproject_files}
%doc README.rst
%{_bindir}/telnetlib3-client
%{_bindir}/telnetlib3-server

%changelog
%autochangelog
