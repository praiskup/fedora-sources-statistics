# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate arbitrary

Name:           rust-arbitrary0.4
Version:        0.4.7
Release:        %autorelease
Summary:        Trait for generating structured data from unstructured data

# Upstream license specification: MIT/Apache-2.0
License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/arbitrary
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
The trait for generating structured data from unstructured data.}

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

%package     -n %{name}+derive-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+derive-devel %{_description}

This package contains library source intended for building other packages which
use the "derive" feature of the "%{crate}" crate.

%files       -n %{name}+derive-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+derive_arbitrary-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+derive_arbitrary-devel %{_description}

This package contains library source intended for building other packages which
use the "derive_arbitrary" feature of the "%{crate}" crate.

%files       -n %{name}+derive_arbitrary-devel
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