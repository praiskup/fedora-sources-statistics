# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate capnpc

Name:           rust-capnpc
Version:        0.19.0
Release:        %autorelease
Summary:        Cap'n Proto code generation

License:        MIT
URL:            https://crates.io/crates/capnpc
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * prevent unused executables from being built and shipped
Patch:          capnpc-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Cap'n Proto code generation.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch
Requires:       /usr/bin/capnp

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
%autosetup -n %{crate}-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires
%if %{with check}
echo '/usr/bin/capnp'
%endif

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