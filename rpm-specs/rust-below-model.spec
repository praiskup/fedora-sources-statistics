# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate below-model

Name:           rust-below-model
Version:        0.8.1
Release:        %autorelease
Summary:        Model crate for below

License:        Apache-2.0
URL:            https://crates.io/crates/below-model
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * bump enum-iterator from 1.4.1 to 2
# * drop unused futures/compat dev-dependency feature
Patch:          below-model-fix-metadata.diff

# Many dependencies not available on 32-bit architectures
ExcludeArch:    %{arm32} %{ix86}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Model crate for below.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
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