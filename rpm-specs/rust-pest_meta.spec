# Generated by rust2rpm 26
# * test grammars are not included in published crates
%bcond_with check
%global debug_package %{nil}

%global crate pest_meta

Name:           rust-pest_meta
Version:        2.7.14
Release:        %autorelease
Summary:        Pest meta language parser and validator

License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/pest_meta
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * drop feature and dependencies for bootstrap build mode
Patch:          pest_meta-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Pest meta language parser and validator.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-APACHE
%license %{crate_instdir}/LICENSE-MIT
%doc %{crate_instdir}/_README.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+grammar-extras-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+grammar-extras-devel %{_description}

This package contains library source intended for building other packages which
use the "grammar-extras" feature of the "%{crate}" crate.

%files       -n %{name}+grammar-extras-devel
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