# Generated by rust2rpm 25
%bcond_without check
%global debug_package %{nil}

%global crate pure-rust-locales

Name:           rust-pure-rust-locales
Version:        0.8.1
Release:        %autorelease
Summary:        Pure Rust locales imported directly from the GNU C Library

License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/pure-rust-locales
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Pure Rust locales imported directly from the GNU C Library. `LC_COLLATE`
and `LC_CTYPE` are not yet supported.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE.Apache-2.0
%license %{crate_instdir}/LICENSE.MIT
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
# skip checking API freshness (only useful for upstream)
%cargo_test -- -- --skip checksum
%endif

%changelog
%autochangelog