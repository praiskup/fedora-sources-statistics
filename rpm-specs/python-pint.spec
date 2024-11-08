%bcond xarray 1
# Not yet packaged: python-uncertainties
%bcond uncertainties 0
# Requires babel <= 2.8; F41 has 2.15.0
%bcond babel 0
# Not yet packaged: python-pint-pandas
%bcond pandas 0
# Not yet packaged: python-mip
%bcond mip 0
# may need to be disabled sometimes for bootstrapping
%bcond dask 1

Name:           python-pint
Version:        0.24.3
Release:        %autorelease
Summary:        Physical quantities module

License:        BSD-3-Clause
URL:            https://github.com/hgrecco/pint
Source:         %{pypi_source pint}

# Workaround from https://github.com/hgrecco/pint/issues/1969
Patch:          dataclass-frozen.patch

BuildArch:      noarch

%global _description %{expand:
Pint is a Python package to define, operate and manipulate physical quantities:
the product of a numerical value and a unit of measurement. It allows
arithmetic operations between them and conversions from and to different units.

It is distributed with a comprehensive list of physical units, prefixes and
constants.}

%description %{_description}

%package -n python3-pint
Summary:        %{summary}

%description -n python3-pint %{_description}

%pyproject_extras_subpkg -n python3-pint numpy
%if %{with xarray}
%pyproject_extras_subpkg -n python3-pint xarray
%endif
%if %{with dask}
%pyproject_extras_subpkg -n python3-pint dask
%endif
%if %{with uncertainties}
%pyproject_extras_subpkg -n python3-pint uncertainties
%endif
%if %{with babel}
%pyproject_extras_subpkg -n python3-pint babel
%endif
%if %{with pandas}
%pyproject_extras_subpkg -n python3-pint pandas
%endif
%if %{with mip}
%pyproject_extras_subpkg -n python3-pint mip
%endif

%prep
%autosetup -n pint-%{version} -p1

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -r -i '/pytest-cov/d' pyproject.toml

# This module is executable in the source, and it might make sense for upstream
# to run it directly as a script during development, but this package will
# install it in site-packages without the executable bit set, so it doesn’t
# make sense for it to have a shebang. Package users will run it via the
# generated pint-convert entry point instead.
sed -r -i '1{/^#!/d}' pint/pint_convert.py

%generate_buildrequires
%{pyproject_buildrequires \
    -x numpy \
%if %{with uncertainties}
    -x uncertainties \
%endif
%if %{with babel}
    -x babel \
%endif
%if %{with pandas}
    -x pandas \
%endif
%if %{with xarray}
    -x xarray \
%endif
%if %{with dask}
    -x dask \
%endif
%if %{with mip}
    -x mip \
%endif
    -x test}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l pint

%check
# -rs: print reasons for skipped tests
%pytest -rs

%files -n python3-pint -f %{pyproject_files}
%{_bindir}/pint-convert

%changelog
%autochangelog
