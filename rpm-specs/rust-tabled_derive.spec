# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate tabled_derive

Name:           rust-tabled_derive
Version:        0.6.0
Release:        %autorelease
Summary:        Derive macros which is used by tabled crate

License:        MIT
URL:            https://crates.io/crates/tabled_derive
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Derive macros which is used by tabled crate.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-MIT
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
%autosetup -n %{crate}-%{version_no_tilde} -p1
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
