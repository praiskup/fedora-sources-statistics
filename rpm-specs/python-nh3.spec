Name:           python-nh3
Version:        0.2.18
Release:        %autorelease
Summary:        Python binding to Ammonia HTML sanitizer Rust crate
License:        MIT
URL:            https://github.com/messense/nh3
Source:         %{pypi_source nh3}

BuildRequires:  cargo-rpm-macros
BuildRequires:  python3-devel

# For tests
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Python binding to Ammonia HTML sanitizer Rust crate.}

# The Python extension module now gets a SONAME of libnh3.so; we
# must ensure it is not used to generate automatic Provides. See:
#   Rust 1.81+ implicitly / automatically sets soname on cdylib targets
#   https://bugzilla.redhat.com/show_bug.cgi?id=2314879
# https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/#_filtering_provides_and_requires_after_scanning
%global __provides_exclude ^libnh3\\.so.*$

%description %_description

%package -n python3-nh3
Summary:        %{summary}
# Full license breakdown in LICENSES.dependencies
License:        MIT AND Apache-2.0 AND (MIT OR Apache-2.0) AND (Zlib OR Apache-2.0 OR MIT)

%description -n python3-nh3 %_description


%prep
%autosetup -p1 -n nh3-%{version}

%cargo_prep


%generate_buildrequires
%pyproject_buildrequires
%cargo_generate_buildrequires


%build
export RUSTFLAGS='%{build_rustflags}'
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files nh3


%check
%pytest -vv


%files -n python3-nh3 -f %{pyproject_files}
%license LICENSE LICENSES.dependencies
%doc README.md


%changelog
%autochangelog
