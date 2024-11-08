# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate tendril

Name:           rust-tendril
Version:        0.4.3
Release:        %autorelease
Summary:        Compact buffer/string type for zero-copy parsing

# Upstream license specification: MIT/Apache-2.0
License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/tendril
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * drop outdated, example-only rand dev-dependency
# * drop unused support for the obsolete "encoding" crate
Patch:          tendril-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Compact buffer/string type for zero-copy parsing.}

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

%package     -n %{name}+bench-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+bench-devel %{_description}

This package contains library source intended for building other packages which
use the "bench" feature of the "%{crate}" crate.

%files       -n %{name}+bench-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+encoding_rs-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+encoding_rs-devel %{_description}

This package contains library source intended for building other packages which
use the "encoding_rs" feature of the "%{crate}" crate.

%files       -n %{name}+encoding_rs-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep
# drop unused example program that pulls in outdated dependencies
rm -rv examples/

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
# * skip test for exact size of a struct / enum that fails with Rust 1.64+:
#   https://github.com/servo/tendril/issues/66
%cargo_test -- -- --skip assert_sizes
%endif

%changelog
%autochangelog
