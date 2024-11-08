%global srcname jiter
%global _description %{summary}.

# The Python extension module now gets a SONAME of libjiter_python.so; we
# must ensure it is not used to generate automatic Provides. See:
#   Rust 1.81+ implicitly / automatically sets soname on cdylib targets
#   https://bugzilla.redhat.com/show_bug.cgi?id=2314879
# https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/#_filtering_provides_and_requires_after_scanning
%global __provides_exclude ^libjiter_python\.so.*$

Name:           python-%{srcname}
Version:        0.5.0
Release:        %autorelease
Summary:        Fast iterable JSON parser

# python-jiter is MIT only, but the rest are rust libraries
# based on cargo_license_summary output:
#
# Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# MIT
# MIT OR Apache-2.0 (duplicate)
License:        %{shrink:
                (Apache-2.0 OR MIT) AND
                (BSD-2-Clause OR Apache-2.0 OR MIT) AND
                MIT
                }
URL:            https://github.com/pydantic/jiter/
Source0:         %{pypi_source %{srcname}}

BuildRequires:  python3-devel
BuildRequires:  tomcli

# For included rust code
BuildRequires:  cargo-rpm-macros

# For tests
BuildRequires:  python3dist(dirty-equals)
BuildRequires:  python3dist(pytest)

%description
%{_description}

%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p1 -n %{srcname}-%{version}
# There is no top-level LICENSE file, but the one from the bundled jiter crate
# is the correct license.
mv crates/jiter/LICENSE ./

# However, we want to use the system copy of the jiter crate.
rm -r crates/jiter

# E.g., for 0.5.0, this would allow 0.5.x.
tomcli set crates/jiter-python/Cargo.toml str dependencies.jiter.version "%{version}"
tomcli set crates/jiter-python/Cargo.toml del dependencies.jiter.path
%cargo_prep


%generate_buildrequires
%cargo_generate_buildrequires -a
%pyproject_buildrequires


%build
%pyproject_wheel

%cargo_license_summary
%{cargo_license} > LICENSE.dependencies


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%pyproject_check_import
%pytest


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE LICENSE.dependencies
%doc README.md


%changelog
%autochangelog