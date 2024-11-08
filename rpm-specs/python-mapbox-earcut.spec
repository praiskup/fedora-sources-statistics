Name:           python-mapbox-earcut
Version:        1.0.2
Release:        %autorelease
Summary:        Python bindings to the mapbox earcut C++ library

# The entire source is (SPDX) ISC; the License also includes the licenses of
# two header-only libraries that are compiled into the extension:
#   - earcut-hpp-static is also ISC
#   - pybind11-static is BSD-3-Clause
License:        ISC AND BSD-3-Clause
URL:            https://github.com/skogler/mapbox_earcut_python
# The GitHub archive contains tests; the PyPI archive does not
Source:         %{url}/archive/v%{version}/mapbox_earcut_python-%{version}.tar.gz

BuildRequires:  python3-devel

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make

# Header-only libraries; -static is for tracking, required by guidelines
# Minimum version added downstream to ensure the latest bug fixes are present.
# Note that upstream of this package bundles earcut.hpp 2.2.4 in release 1.0.1.
BuildRequires:  earcut-hpp-devel >= 2.2.4
BuildRequires:  earcut-hpp-static
# An extension built with pybind11 uses the pybind11 C++ libraries, which are
# header-only—so, strictly speaking, we need this as well:
BuildRequires:  pybind11-static

BuildRequires:  dos2unix

%global common_description %{expand:
Python bindings for the C++ implementation of the Mapbox Earcut library, which
provides very fast and quite robust triangulation of 2D polygons.

Original code: earcut.hpp

Original description:

    The library implements a modified ear slicing algorithm, optimized by
    z-order curve hashing and extended to handle holes, twisted polygons,
    degeneracies and self-intersections in a way that doesn’t guarantee
    correctness of triangulation, but attempts to always produce acceptable
    results for practical data like geographical shapes.}

%description %{common_description}


%package -n python3-mapbox-earcut
Summary:        %{summary}

%description -n python3-mapbox-earcut %{common_description}


%prep
%autosetup -n mapbox_earcut_python-%{version}

# Remove bundled earcut.hpp library
rm -rvf include

# Fix CRLF line endings in files that will be installed.
dos2unix --keepdate *.md


%generate_buildrequires
%pyproject_buildrequires -x test


%build
# See comments in the earcut-hpp spec file, as well as:
# https://github.com/mapbox/earcut.hpp/issues/97
# https://github.com/mapbox/earcut.hpp/issues/103
export CFLAGS="${CFLAGS-} -ffp-contract=off"
export CXXFLAGS="${CXXFLAGS-} -ffp-contract=off"

%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l mapbox_earcut


%check
%pytest


%files -n python3-mapbox-earcut -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
