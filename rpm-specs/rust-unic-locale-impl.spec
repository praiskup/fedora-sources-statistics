# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate unic-locale-impl

Name:           rust-unic-locale-impl
Version:        0.9.5
Release:        %autorelease
Summary:        API for managing Unicode Locale Identifiers

License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/unic-locale-impl
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * drop unused, benchmark-only criterion dev-dependency
Patch:          unic-locale-impl-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
API for managing Unicode Locale Identifiers.}

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
%doc %{crate_instdir}/README.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+likelysubtags-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+likelysubtags-devel %{_description}

This package contains library source intended for building other packages which
use the "likelysubtags" feature of the "%{crate}" crate.

%files       -n %{name}+likelysubtags-devel
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
# * skip a test that requires a files not included in published crates
%cargo_test -- -- --exact --skip parse --skip serialize
%endif

%changelog
%autochangelog