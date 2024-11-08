Name:           python-xxhash
Version:        3.5.0
Release:        %autorelease
Summary:        Python Binding for xxHash

# The entire source is BSD-2-Clause. When the PyPI sdist is used (vs. the
# GitHub archive), a bundled copy of portions of the xxhash C library is also
# present in the source archive; it is under the same license and is removed in
# %%prep.
License:        BSD-2-Clause
URL:            https://github.com/ifduyue/python-xxhash
Source:         %{pypi_source xxhash}

BuildRequires:  python3-devel

BuildRequires:  gcc
BuildRequires:  pkgconfig(libxxhash) >= 0.8.2

%global common_description %{expand:
xxhash is a Python binding for the xxHash library by Yann Collet.}

%description %{common_description}


%package -n python3-xxhash
Summary:        %{summary}

%description -n python3-xxhash %{common_description}


%prep
%autosetup -n xxhash-%{version}
# Remove bundled xxhash library
rm -rvf deps


%generate_buildrequires
%pyproject_buildrequires


%build
# Normally, no extra flags are required to link the xxhash shared library, but
# we are prepared:
export CFLAGS="${CFLAGS} $(pkgconf --cflags libxxhash)"
export LDFLAGS="${LDFLAGS} $(pkgconf --libs-only-L libxxhash)"
export LDFLAGS="${LDFLAGS} $(pkgconf --libs-only-other libxxhash)"
export XXHASH_LINK_SO='1'
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l xxhash


%check
cd tests
%{py3_test_envvars} %{python3} -m unittest discover


%files -n python3-xxhash -f %{pyproject_files}
%doc CHANGELOG.rst
%doc README.rst


%changelog
%autochangelog
