# Upstream version is 2.0.1 but has no release
%global snapdate 20240820
%global commit e988a5ffc9abb8010fc75dba54904d1c5dbe83db
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# set upstream name variable
%global srcname pyDes


Name:           python-pydes
Version:        2.0.1^%{snapdate}git%{shortcommit}
Release:        %autorelease
Summary:        Pure python implementation of DES and TRIPLE DES encryption algorithm

License:        MIT
URL:            https://github.com/twhiteman/%{srcname}
Source0:        %{url}/archive/%{commit}/%{srcname}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
This is a pure python implementation of the DES encryption
algorithm. It's pure python to avoid portability issues, since most
DES implementations are programmed in C (for performance reasons).}

%description %{_description}


%package     -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname}-%{commit}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{srcname}


%check
%pyproject_check_import
# Tests suite cannot be launched with pytest
%{__python3} test_pydes.py


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
