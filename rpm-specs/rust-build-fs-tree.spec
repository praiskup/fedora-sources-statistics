# Generated by rust2rpm 25
%bcond_without check
%global debug_package %{nil}

%global crate build-fs-tree

Name:           rust-build-fs-tree
Version:        0.6.0
Release:        %autorelease
Summary:        Generate a filesystem tree from a macro or a YAML tree

License:        MIT
URL:            https://crates.io/crates/build-fs-tree
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
Patch:          build-fs-tree-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Generate a filesystem tree from a macro or a YAML tree.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE.md
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

%package     -n %{name}+clap-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+clap-devel %{_description}

This package contains library source intended for building other packages which
use the "clap" feature of the "%{crate}" crate.

%files       -n %{name}+clap-devel
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