# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate listenfd

Name:           rust-listenfd
Version:        1.0.1
Release:        %autorelease
Summary:        Simple library to work with listenfds passed from the outside

License:        Apache-2.0
URL:            https://crates.io/crates/listenfd
Source:         %{crates_source}
# Automatically generated patch to strip foreign dependencies
Patch:          listenfd-fix-metadata-auto.diff

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
A simple library to work with listenfds passed from the outside
(systemd/catflap socket activation).}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
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
