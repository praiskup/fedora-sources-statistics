%global pypi_name freetype-py

Name:           python-freetype
Version:        2.5.1
Release:        %autorelease
Summary:        Python binding for the freetype library
License:        BSD-3-Clause
URL:            https://github.com/rougier/freetype-py
Source0: 	%{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
# tests use tox
BuildRequires:  python3dist(tox-current-env)
BuildRequires:  python3dist(pytest)

BuildRequires:  freetype

%description
Freetype Python provides bindings for the FreeType library. Only the high-level
API is bound.

%package -n     python3-freetype
Summary:        %{summary}
%py_provides python3-freetype

%description -n python3-freetype
%{description}

%prep
%autosetup -n %{pypi_name}-%{version}

%py3_shebang_fix freetype/*.py
%py3_shebang_fix examples/*.py

sed -i 's/"setuptools_scm\[toml\]>=3.4",//' pyproject.toml
sed -i 's/"certifi",//' pyproject.toml
sed -i 's/"cmake"//' pyproject.toml

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l freetype

%check
%tox

%files -n python3-freetype -f %{pyproject_files}
%doc examples README.rst

%changelog
%autochangelog
