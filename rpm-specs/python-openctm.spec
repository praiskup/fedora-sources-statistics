Name:           python-openctm
Version:        0.0.6
Release:        %autorelease
Summary:        Provide a loader for OpenCTM files

License:        MIT
URL:            https://github.com/trimesh/openctm
# The PyPI project does not have sdists, so we must use the GitHub archive.
Source:         %{url}/archive/%{version}/openctm-%{version}.tar.gz

# Downstream-only: use the system OpenCTM library
# Upstream has good reason to bundle this for distribution on PyPI. We raised
# the possibility of upstreaming a version of this patch in
# https://github.com/trimesh/openctm/pull/2#issuecomment-2046008584.
Patch:          0001-Downstream-only-use-the-system-OpenCTM-library.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%global common_description %{expand:
A wheel-packaged binding for OpenCTM Python bindings.}

%description %{common_description}


%package -n python3-openctm
Summary:        %{summary}

Requires:       OpenCTM-libs
# For import “smoke test”
BuildRequires:  OpenCTM-libs

%description -n python3-openctm %{common_description}


%prep
%autosetup -n openctm-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l openctm


%check
# Upstream currently provides no tests.
%pyproject_check_import


%files -n python3-openctm -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
