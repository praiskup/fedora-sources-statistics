# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate below-store

Name:           rust-below-store
Version:        0.8.1
Release:        %autorelease
Summary:        Store crate for below

License:        Apache-2.0
URL:            https://crates.io/crates/below-store
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * bump nix from 0.25 to 0.26
# * enable no-vendor feature by default
# * add zstd as a dependency as well for no-vendor
Patch:          below-store-fix-metadata.diff

# below-model not available
ExcludeArch:    %{arm32} %{ix86}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Store crate for below.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+no-vendor-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+no-vendor-devel %{_description}

This package contains library source intended for building other packages which
use the "no-vendor" feature of the "%{crate}" crate.

%files       -n %{name}+no-vendor-devel
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
%cargo_test
%endif

%changelog
%autochangelog