%global forgeurl https://github.com/jonathf/numpoly

Name:       python-numpoly
Version:    1.2.13
Release:    %autorelease
Summary:    Polynomials as a numpy datatype
%forgemeta
# SPDX
License:    BSD-2-Clause
URL:        %forgeurl
Source:     %forgesource

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(sympy)

%global desc %{expand: \
Numpoly is a generic library for creating, manipulating and evaluating
arrays of polynomials based on `numpy.ndarray` objects.

- Intuitive interface for users experienced with numpy, as the library
  provides a high level of compatibility with the `numpy.ndarray`,
  including fancy indexing, broadcasting, `numpy.dtype`, vectorized
  operations to name a few
- Computationally fast evaluations of lots of functionality inherent
  from numpy
- Vectorized polynomial evaluation
- Support for arbitrary number of dimensions
- Native support for lots of `numpy.<name>` functions using numpy’s
  compatibility layer (which also exists as `numpoly.<name`> equivalents)
- Support for polynomial division through the operators `/`, `%` and
  `divmod`
- Extra polynomial specific attributes exposed on the polynomial
  objects like `poly.exponents`, `poly.coefficients`,
  `poly.indeterminants` etc.
- Polynomial derivation through functions like `numpoly.derivative`,
  `numpoly.gradient`, `numpoly.hessian` etc.
- Decompose polynomial sums into vector of addends using
  `numpoly.decompose`
- Variable substitution through `numpoly.call`}

%description
%{desc}

%package -n     python3-numpoly
Summary:        %{summary}

%description -n python3-numpoly
%{desc}

%prep
%forgeautosetup -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l numpoly

%check
%pytest -v

%files -n python3-numpoly -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
