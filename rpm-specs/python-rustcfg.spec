%global srcname rustcfg
%{?python_enable_dependency_generator}

Name:           python-rustcfg
Version:        0.0.2
Release:        %autorelease
Summary:        Rust cfg expression parser in python

License:        MIT
URL:            https://pagure.io/fedora-rust/python-rustcfg
Source:         %{pypi_source}

BuildArch:      noarch

%global _description \
%{summary}.

%description %_description

%package     -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3dist(pyparsing)
BuildRequires:  python3-pytest

%description -n python3-%{srcname} %{_description}

%package     -n python3-%{srcname}-tests
Summary:        Tests for python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}-tests}
Requires:       python3-%{srcname} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-pytest

%description -n python3-rustcfg-tests
%{summary}.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
py.test-%{python3_version} -v

%files -n python3-%{srcname}
%license LICENSE
%{python3_sitelib}/rustcfg-*.egg-info/
%{python3_sitelib}/rustcfg/
%exclude %{python3_sitelib}/rustcfg/test

%files -n python3-%{srcname}-tests
%{python3_sitelib}/%{srcname}/test/

%changelog
%autochangelog
