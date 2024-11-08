# Generated by rust2rpm 25
%bcond_without check
%global debug_package %{nil}

%global crate uncased

Name:           rust-uncased
Version:        0.9.10
Release:        %autorelease
Summary:        Case-preserving, ASCII case-insensitive, no_std string types

License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/uncased
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Case-preserving, ASCII case-insensitive, no_std string types.}

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

%package     -n %{name}+alloc-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+alloc-devel %{_description}

This package contains library source intended for building other packages which
use the "alloc" feature of the "%{crate}" crate.

%files       -n %{name}+alloc-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+serde-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+serde-devel %{_description}

This package contains library source intended for building other packages which
use the "serde" feature of the "%{crate}" crate.

%files       -n %{name}+serde-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+with-serde-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+with-serde-devel %{_description}

This package contains library source intended for building other packages which
use the "with-serde" feature of the "%{crate}" crate.

%files       -n %{name}+with-serde-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+with-serde-alloc-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+with-serde-alloc-devel %{_description}

This package contains library source intended for building other packages which
use the "with-serde-alloc" feature of the "%{crate}" crate.

%files       -n %{name}+with-serde-alloc-devel
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
%cargo_test
%endif

%changelog
%autochangelog
