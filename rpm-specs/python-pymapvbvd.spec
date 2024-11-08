Name:           python-pymapvbvd
Version:        0.6.0
Release:        %autorelease
Summary:        Python twix file reader

# The entire source is MIT, except:
#   - The file pymapvbvd/_version.py, which is generated by python-versioneer,
#     shares its license (Unlicense, for recent versions of Versioneer); see
#     also versioneer.py (which is removed in %%prep)
License:        MIT AND Unlicense
URL:            https://github.com/wtclarke/pymapvbvd
Source0:        %{pypi_source pymapvbvd}
# Generated with Source2: ./get_test_data.sh %%{version}
Source1:        pymapvbvd-test-data.tar.zst
Source2:        get_test_data.sh

# Downstream-only: do not pin the scipy version (and allow 0.11.x)
Patch:          0001-Downstream-only-do-not-pin-the-scipy-version-and-all.patch

BuildArch:      noarch
# PyMapVBVD assumes the platform is little-endian
# https://bugzilla.redhat.com/show_bug.cgi?id=2225518
ExcludeArch:    s390x

BuildRequires:  python3-devel

%global common_description %{expand:
Python port of the Matlab mapVBVD tool for reading Siemens raw data 'twix'
(.dat) files.}

%description %{common_description}


%package -n python3-pymapvbvd
Summary:        %{summary}

# Provides for the actual importable module name, which is unfortunately
# different from the PyPI package name (pyMapVBVD).
%py_provides python3-mapvbvd

# The generated _version.py has the same license as python3dist(versioneer),
# but we do not consider it to be bundled from Versioneer.

%description -n python3-pymapvbvd %{common_description}


%prep
%autosetup -n pymapvbvd-%{version} -p1
%setup -q -T -D -a 1 -c -n pymapvbvd-%{version}
# We can use the system versioneer to generate _version.py, and can remove the
# bundled, amaglamated versioneer.py to indicate we aren’t using it.
rm -v versioneer.py


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_buildrequires -x tests


%build
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l mapvbvd


%check
%pytest -v


%files -n python3-pymapvbvd -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
