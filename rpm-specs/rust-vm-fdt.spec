# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate vm-fdt

Name:           rust-vm-fdt
Version:        0.3.0
Release:        %autorelease
Summary:        For writing Flattened Devicetree blobs

License:        Apache-2.0 OR BSD-3-Clause
URL:            https://crates.io/crates/vm-fdt
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * exclude maintainer-only files from the package
Patch:          vm-fdt-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Crate for writing Flattened Devicetree blobs.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-APACHE
%license %{crate_instdir}/LICENSE-BSD-3-Clause
%doc %{crate_instdir}/CHANGELOG.md
%doc %{crate_instdir}/README.md
%doc %{crate_instdir}/img
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+alloc-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+alloc-devel %{_description}

This package contains library source intended for building other packages which
use the "alloc" feature of the "%{crate}" crate.

%files       -n %{name}+alloc-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+hashbrown-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+hashbrown-devel %{_description}

This package contains library source intended for building other packages which
use the "hashbrown" feature of the "%{crate}" crate.

%files       -n %{name}+hashbrown-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+long_running_test-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+long_running_test-devel %{_description}

This package contains library source intended for building other packages which
use the "long_running_test" feature of the "%{crate}" crate.

%files       -n %{name}+long_running_test-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+std-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+std-devel %{_description}

This package contains library source intended for building other packages which
use the "std" feature of the "%{crate}" crate.

%files       -n %{name}+std-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%ifarch %{ix86}
# * skip overflow test on 32-bit targets (for causing capacity overflow panic)
%cargo_test -f long_running_test -- -- --exact --skip=writer::tests::test_overflow_subtract
%else
%cargo_test -f long_running_test
%endif
%endif

%changelog
%autochangelog