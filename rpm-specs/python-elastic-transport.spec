%global srcname elastic-transport
%global _desc %{expand: \
Transport classes and utilities shared among Python Elastic client libraries

This library was lifted from elasticsearch-py and then transformed to be used
across all Elastic services rather than only Elasticsearch.}

Name:		python-%{srcname}
Version:	8.13.1
Release:	%autorelease
Summary:	Transport classes and utilities shared among Python Elastic

License:	Apache-2.0
URL:		https://github.com/elastic/elastic-transport-python
Source0:	%{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

Patch0:		remove-mock.patch

BuildArch:	noarch

BuildRequires:	python3-devel
BuildRequires:	python3-pytest

%description %{_desc}

%package -n python3-%{srcname}
Summary:	%{summary}

%description -n python3-%{srcname} %{_desc}

%prep
%autosetup -p1 -n %{srcname}-python-%{version}

%generate_buildrequires
%pyproject_buildrequires -r -x develop

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files elastic_transport

%check
%pytest -v -k 'not test_http_aiohttp and not test_urllib3_chain_certs and not test_tls_versions and not test_ssl_assert_fingerprint and not httpx'

%files -n python3-%{srcname} -f %{pyproject_files}
%doc CHANGELOG.md README.md

%changelog
%autochangelog
