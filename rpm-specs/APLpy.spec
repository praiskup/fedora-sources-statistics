%global srcname APLpy

Name:           APLpy
Version:        2.0.3
Release:        %autorelease
Summary:        The Astronomical Plotting Library in Python

License:        MIT
URL:            http://aplpy.github.com
Source0:        %{pypi_source}
Patch0:         aplpy-moved-function.patch
# https://github.com/aplpy/aplpy/pull/469
Patch1:         aplpy-wraps-from-functools.patch
# Workaround for python 3.12 change of imp module removal
Patch2:         astropy_helpers-py312-imp-deprecation.patch
# related:
# https://github.com/astropy/astropy/pull/12633
# astropy 5.1 removes astropy.tests.plugins.display and so on
Patch3:         aplpy-astropy-5.1-tests-plugins-removal.patch
Patch4:         aplpy-deps.patch
# https://github.com/aplpy/aplpy/pull/500
Patch5:         0001-Fix-cmap-handling-with-Matplotlib-3.9.patch

BuildArch:      noarch
BuildRequires:  python3-devel 

%description
APLpy (the Astronomical Plotting Library in Python) is a Python module aimed at 
producing publication-quality plots of astronomical imaging data in FITS format.
The module uses Matplotlib, a powerful and interactive plotting package. It is
capable of creating output files in several graphical formats, including EPS,
PDF, PS, PNG, and SVG.

%package -n python3-APLpy
Summary:        The Astronomical Plotting Library in Python
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-setuptools

%description -n python3-APLpy
APLpy (the Astronomical Plotting Library in Python) is a Python module aimed at 
producing publication-quality plots of astronomical imaging data in FITS format.
The module uses Matplotlib, a powerful and interactive plotting package. It is
capable of creating output files in several graphical formats, including EPS,
PDF, PS, PNG, and SVG.

%prep
%autosetup -n %{srcname}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install 

%pyproject_save_files -l aplpy

%check
%pyproject_check_import -t


%files -n python3-APLpy -f %{pyproject_files}
%doc CHANGES.rst README.rst

%changelog
%autochangelog
