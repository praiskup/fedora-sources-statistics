# Generated by rust2rpm 25
%bcond_without check
%global debug_package %{nil}

%global crate sanitize-filename

Name:           rust-sanitize-filename
Version:        0.5.0
Release:        %autorelease
Summary:        Simple filename sanitizer, based on Node's sanitize-filename

License:        MIT
URL:            https://crates.io/crates/sanitize-filename
Source:         %{crates_source}
# Upstream PR: https://github.com/kardeiz/sanitize-filename/pull/10
Source1:        https://raw.githubusercontent.com/kardeiz/sanitize-filename/ee35c34ce6f867643a13265e24dc95fd7ca31dc5/LICENSE
# Manually created patch for downstream crate metadata changes
# * Deactivate binary compilation, since we are not interested in the binary
Patch:          sanitize-filename-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
A simple filename sanitizer, based on Node's sanitize-filename.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
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
cp -pv %{SOURCE1} .
find . -type f -exec chmod -x {} \;
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
