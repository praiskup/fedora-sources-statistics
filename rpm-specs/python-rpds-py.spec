%global srcname rpds-py
%global modname rpds_py

Name:           python-rpds-py
Version:        0.20.0
Release:        %autorelease
Summary:        Python bindings to the Rust rpds crate
# Full license breakdown in LICENSES.dependencies
License:        MIT AND Apache-2.0 AND (MIT OR Apache-2.0) AND MPL-2.0
URL:            https://github.com/crate-py/rpds
Source:         %{pypi_source %{modname}}

# The 'generate-import-lib' extension is only useful on MS Win
Patch:          do_not_require_win_only_pyo3_extension.patch

BuildRequires:  cargo-rpm-macros
BuildRequires:  dos2unix
BuildRequires:  python3-devel

# The Python extension module now gets a SONAME of librpds.so; we
# must ensure it is not used to generate automatic Provides. See:
#   Rust 1.81+ implicitly / automatically sets soname on cdylib targets
#   https://bugzilla.redhat.com/show_bug.cgi?id=2314879
# https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/#_filtering_provides_and_requires_after_scanning
%global __provides_exclude ^librpds\\.so.*$

%global _description %{expand:
Python bindings to the Rust rpds crate.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description


%prep
%autosetup -p1 -n %{modname}-%{version}

# Fix line terminations
dos2unix README* LICENSE* *.pyi

# Fix for bad requirements dependency
sed -r -i 's/^file:/# &/' tests/requirements.in

%cargo_prep


%generate_buildrequires
%pyproject_buildrequires tests/requirements.in
%cargo_generate_buildrequires


%build
export RUSTFLAGS='%{build_rustflags}'
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files rpds


%check
%pytest -vv


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE LICENSES.dependencies
%doc README.rst


%changelog
%autochangelog
