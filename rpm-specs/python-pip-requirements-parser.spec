%global pypi_name pip-requirements-parser
%global pypi_name_with_underscore %(echo "%{pypi_name}" | sed "s/-/_/g")

Name:           python-%{pypi_name}
Version:        32.0.1
Release:        %autorelease
Summary:        Mostly correct pip requirements parsing library

# Clarification asked
# https://github.com/nexB/pip-requirements-parser/issues/21
License:        MIT AND (BSD-2-Clause OR Apache-2.0)
URL:            https://github.com/nexB/pip-requirements-parser
Source:         %url/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)

%global common_description %{expand:
pip-requirements-parser is a mostly correct pip requirements parsing library...
because it uses pip's own code.

pip is the package installer for Python that is using "requirements" text files
listing the packages to install.}

%description %{common_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{common_description}

%package -n python-%{pypi_name}-doc
Summary:        Documentation for python-%{pypi_name}
# BSD-2-Clause: Sphinx javascript
# MIT: jquery
License:        MIT AND BSD-2-Clause
BuildArch:      noarch
Requires:       python3-%{pypi_name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(js-sphinx_javascript_frameworks_compat)
Provides:       bundled(js-doctools)
Provides:       bundled(js-jquery)
Provides:       bundled(js-language_data)
Provides:       bundled(js-searchtools)

%description -n python-%{pypi_name}-doc
%{common_description}

This package is providing the documentation for %{pypi_name}.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
sed -i 's|\(fallback_version = "\)[^"]*|\1%{version}|' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires
%build
%pyproject_wheel

# generate html docs
sphinx-build-3 -b html docs/source html
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%pyproject_install
%pyproject_save_files %{pypi_name_with_underscore}

%check
# https://github.com/nexB/pip-requirements-parser/issues/22
%pytest -k 'not test_RequirementsFile_to_dict and not test_RequirementsFile_dumps_unparse'

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc AUTHORS.rst AUTHORS.txt CHANGELOG.rst README.rst
%pycached %{python3_sitelib}/packaging_legacy_version.py

%files -n python-%{pypi_name}-doc
%doc html

%changelog
%autochangelog
