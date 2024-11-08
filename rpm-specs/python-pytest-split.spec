%bcond tests 1
%global srcname pytest-split
%global slugname pytest_split

Name:           python-%{srcname}
Summary:        Pytest plugin to split the test suite into sub-suites
Version:        0.10.0
Release:        %autorelease

License:         MIT
URL:             https://github.com/jerry-git/pytest-split
Source:          %{url}/archive/refs/tags/%{version}/%{srcname}-%{version}.tar.gz
BuildArch:       noarch

BuildRequires:   python3-devel
BuildRequires:   help2man
BuildRequires:   python3dist(poetry-core)
BuildRequires:   python3dist(pytest)
BuildRequires:   python3dist(pytest-cov)
Requires:        python3dist(pytest)

%global _description %{expand:
Pytest plugin which splits the test suite to equally sized
sub suites based on test execution time.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
mkdir -p %{buildroot}%{_mandir}/man1
PYTHONPATH="%{buildroot}%{python3_sitelib}" help2man \
    --version-string %{version} \
    %{buildroot}%{_bindir}/slowest-tests | \
    gzip > %{buildroot}%{_mandir}/man1/slowest-tests.1.gz

%check
%py3_check_import %{slugname}

%if %{with tests}
%pytest --no-cov tests
%endif

%files -n python3-%{srcname}
%doc README.md
%doc CHANGELOG.md
%license LICENSE
%{python3_sitelib}/%{slugname}-%{version}.dist-info/
%{python3_sitelib}/%{slugname}/
%{_bindir}/slowest-tests
%{_mandir}/man1/slowest-tests.1.*

%changelog
%autochangelog
