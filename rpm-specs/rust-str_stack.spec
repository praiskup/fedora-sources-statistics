# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate str_stack

Name:           rust-str_stack
Version:        0.1.0
Release:        %autorelease
Summary:        String allocator for allocating many write-once strings

# Upstream license specification: MIT/Apache-2.0
License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/str_stack
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
A string allocator for allocating many write-once strings. This library
is primarily useful for parsing where you need to repeatedly build many
strings, use them, and then throw them away. Instead of allocating many
independent strings, this library will put them all in the same buffer.}

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