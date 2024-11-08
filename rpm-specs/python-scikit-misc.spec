%global pypi_name scikit-misc
# Use GitHub sources. PyPI sources are not suitable for rebuilding.
# https://github.com/has2k1/scikit-misc/issues/27
%global forgeurl https://github.com/has2k1/scikit-misc

# Enable tests
%bcond tests 1

Name:           python-%{pypi_name}
Version:        0.5.1
Release:        %autorelease
Summary:        Miscellaneous tools for data analysis and scientific computing

%forgemeta

# MIT License applies to doc/theme/static/bootstrap-3.4.1
# Python-2.0.1 license applies to doc/_static/copybutton.js
License:        BSD-3-Clause AND MIT AND Python-2.0.1
URL:            %forgeurl
Source:         %forgesource

ExcludeArch:    %{ix86}
BuildRequires:  gcc-gfortran
BuildRequires:  git-core
BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-pytest
%endif

%global _description %{expand:
Miscellaneous tools for data analysis and scientific computing.}

%description %_description


%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %_description


%prep
%forgeautosetup -S git
# Supply the version information to mesonpy
git tag v%{version}

%py3_shebang_fix spin skmisc/_build_utils/

# Disable coverage
sed -i -e 's/--cov=skmisc --cov-report=xml//' pyproject.toml

# Do not attempt to build with numpy>=2.0
sed -r -i 's/(numpy)>=2.0/\1/' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -w

# There is no build section since the wheel is already build as part of
# %%pyproject_buildrequires

%install
%pyproject_install
%pyproject_save_files skmisc


%check
%if %{with tests}
  # pytest >= 8 wants to import from the skmisc/ src dir
  mkdir empty && pushd empty
  ln -s ../skmisc/loess/tests .
  %pytest -v --pyargs --import-mode=importlib
%else
  %pyproject_check_import
%endif


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
%autochangelog
