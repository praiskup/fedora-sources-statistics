# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate hostname-validator

Name:           rust-hostname-validator
Version:        1.1.1
Release:        %autorelease
Summary:        Validate hostnames according to IETF RFC 1123

License:        MIT
URL:            https://crates.io/crates/hostname-validator
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Validate hostnames according to IETF RFC 1123.}

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