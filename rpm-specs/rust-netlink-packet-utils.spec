# Generated by rust2rpm 24
# Test is disabled due to upstream bug:
# https://github.com/rust-netlink/netlink-packet-utils/issues/8
%bcond_with check
%global debug_package %{nil}

%global crate netlink-packet-utils

Name:           rust-netlink-packet-utils
Version:        0.5.2
Release:        %autorelease
Summary:        Macros and helpers for parsing netlink messages

License:        MIT
URL:            https://crates.io/crates/netlink-packet-utils
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Macros and helpers for parsing netlink messages.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-MIT
%doc %{crate_instdir}/CHANGELOG
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