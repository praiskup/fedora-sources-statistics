%global srcname elasticsearch
%global _desc %{expand: \
Low level client for Elasticsearch. It's goal is to provide common ground\
for all Elasticsearch-related code in Python. The client's features include:\
\
- Translating basic Python data types to and from json\
- Configurable automatic discovery of cluster nodes\
- Persistent connections\
- Load balancing (with pluggable selection strategy) across all available nodes\
- Failed connection penalization (time based - failed connections wont be\
  retried until a timeout is reached)\
- Thread safety\
- Pluggable architecture.}

Name:		python-elasticsearch
Version:	8.14.0
Release:	%autorelease
Summary:	Client for Elasticsearch

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:	Apache-2.0
URL:		https://github.com/elasticsearch/elasticsearch-py
Source0:	%{url}/archive/v%{version}/%{srcname}-py-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel
BuildRequires:	python3-sphinx_rtd_theme

%description %{_desc}

%package -n python3-%{srcname}
Summary:	Python 3 Client for Elasticsearch

%description -n python3-%{srcname} %{_desc}

%package -n python-%{srcname}-doc
Summary:    Documentation for Python Elasticsearch

%description -n python-%{srcname}-doc
%{summary}

%prep
%autosetup -n %{srcname}-py-%{version}

sed -i '/addopts/d' setup.cfg
# remove very old missing dep
sed -i '/unasync/d' dev-requirements.txt
# formatter used upstream to generate examples; we don't need it
sed -i '/black/d' dev-requirements.txt
# Test dependencies we don't have yet in Fedora
sed -i '/mapbox-vector-tile/d' dev-requirements.txt
sed -i '/simsimd/d' dev-requirements.txt

%generate_buildrequires
%pyproject_buildrequires -x extras dev-requirements.txt

%build
%pyproject_wheel

# Generate the HTML documentation.
PYTHONPATH=${PWD} sphinx-build-3 docs/sphinx html
# Remove the sphinx-build leftovers.
rm -rf html/.{doctrees,buildinfo}

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%pytest -v

%files -n python3-%{srcname} -f %{pyproject_files}
%doc CHANGELOG.md CONTRIBUTING.md README.rst

%files -n python-%{srcname}-doc
%license LICENSE
%doc html examples 

%changelog
%autochangelog
