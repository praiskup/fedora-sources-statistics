%bcond_without check
%global srcname aw-client

Name:           python-%{srcname}
Version:        0.5.13
Release:        %autorelease
Summary:        Client library for ActivityWatch in Python

License:        MPL-2.0
URL:            https://github.com/ActivityWatch/aw-client
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Client library for ActivityWatch in Python.}

%description %{_description}

%package -n python3-%{srcname}
Summary:    %{summary}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files aw_client

%check
# skip test_client.py due to a http connection error
# skip test_failqueue.py due to missing aw_server dependency
%pytest --ignore=tests/test_client.py \
        --ignore=tests/test_failqueue.py

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license LICENSE.txt
%{_bindir}/aw-client

%changelog
%autochangelog
