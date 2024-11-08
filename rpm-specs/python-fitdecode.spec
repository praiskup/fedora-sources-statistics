%global srcname fitdecode

Name:           python-%{srcname}
Version:        0.10.0
Release:        %autorelease
Summary:        FIT file parser and decoder

License:        MIT
URL:            https://github.com/polyvertex/fitdecode
# PyPI tarball doesn't include tests
Source:         %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%global _description %{expand:
This package provides a FIT file parsing and decoding library for Python.}

%description %_description

%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst HISTORY.rst
%{_bindir}/fitjson
%{_bindir}/fittxt

%changelog
%autochangelog
