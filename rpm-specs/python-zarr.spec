%global srcname zarr

Name:           python-%{srcname}
Version:        2.16.1
Release:        %autorelease
Summary:        Chunked, compressed, N-dimensional arrays for Python

License:        MIT
URL:            https://github.com/zarr-developers/zarr
Source0:        %{pypi_source}
# https://github.com/zarr-developers/zarr-python/pull/1970
# https://github.com/zarr-developers/zarr-python/issues/1819
# fix tests with recent fsspec
Patch:          0001-Adapt-storage-tests-for-changes-in-fsspec-1819-1679.patch
# https://github.com/zarr-developers/zarr-python/pull/1972
# https://github.com/zarr-developers/zarr-python/issues/1678
# fix tests with zlib-ng
Patch:          0001-array-tests-handle-different-hexdigests-from-zlib-ng.patch

BuildArch:      noarch

BuildRequires:  python3-devel
# Test dependencies
BuildRequires:  python3dist(bsddb3)
BuildRequires:  python3dist(fsspec)
BuildRequires:  python3dist(h5py)
# lmdb is FTBFS and FTI: https://bugzilla.redhat.com/show_bug.cgi?id=2259530
# not having it causes several tests to be skipped
#BuildRequires:  python3dist(lmdb)
BuildRequires:  python3dist(msgpack)
BuildRequires:  python3dist(pytest)

%description
Zarr is a Python package providing an implementation of compressed, chunked,
N-dimensional arrays, designed for use in parallel computing.


%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname}
Zarr is a Python package providing an implementation of compressed, chunked,
N-dimensional arrays, designed for use in parallel computing.


%package -n python-%{srcname}-doc
Summary:        zarr documentation

BuildArch:      noarch

BuildRequires:  python3dist(numpydoc)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-copybutton)
BuildRequires:  python3dist(sphinx-design)
BuildRequires:  python3dist(sphinx-issues)
BuildRequires:  python3dist(pydata-sphinx-theme)

%description -n python-%{srcname}-doc
Documentation for zarr


%prep
%autosetup -n %{srcname}-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel

# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo,_static/donotdelete}


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%pytest -ra


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.txt
%doc README.md

%files -n python-%{srcname}-doc
%doc html
%license LICENSE.txt


%changelog
%autochangelog