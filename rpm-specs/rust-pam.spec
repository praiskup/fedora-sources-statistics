# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate pam

Name:           rust-pam
Version:        0.7.0
Release:        %autorelease
Summary:        Safe Rust wrappers for PAM authentication

License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/pam
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * bump users dependency from ^0.8 to ^0.10,
# * bump rpassword dev-dependency from ^2 to ^5:
#   https://github.com/1wilkens/pam/pull/21
Patch:          pam-fix-metadata.diff
# Fixing doctest and library name, PR not needed as fixed upstream
Patch:          pam-fix-authenticator.diff

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Safe Rust wrappers for PAM authentication.}

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
%doc %{crate_instdir}/CHANGELOG.md
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