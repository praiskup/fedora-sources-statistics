# Created by pyp2rpm-3.3.10
%global srcname sphinx-autoapi
%global srcname_ sphinx_autoapi

Name:           python-%{srcname}
Version:        3.2.1
Release:        %autorelease
Summary:        Sphinx API documentation generator

License:        MIT
URL:            https://github.com/readthedocs/sphinx-autoapi
Source:         %pypi_source %{srcname_}
# https://github.com/readthedocs/sphinx-autoapi/pull/462
Patch:          0001-Mark-tests-that-use-the-network.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(beautifulsoup4)
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Sphinx AutoAPI is a Sphinx extension for generating complete API documentation
without needing to load, run, or import the project being documented.

In contrast to the traditional Sphinx autodoc, which requires manual authoring
and uses code imports, AutoAPI finds and generates documentation by parsing
source code.}

%description %{_description}

%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname_}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files -l autoapi

%check
%{pytest} -m 'not network'

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
