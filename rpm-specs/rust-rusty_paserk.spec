# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate rusty_paserk

Name:           rust-rusty_paserk
Version:        0.4.0
Release:        %autorelease
Summary:        Platform Agnostic Serializable Keys

License:        MIT
URL:            https://crates.io/crates/rusty_paserk
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Platform Agnostic Serializable Keys (PASERK) is an extension on PASETO
for key management.}

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
%doc %{crate_instdir}/SECURITY.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+arbitrary-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+arbitrary-devel %{_description}

This package contains library source intended for building other packages which
use the "arbitrary" feature of the "%{crate}" crate.

%files       -n %{name}+arbitrary-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+serde-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+serde-devel %{_description}

This package contains library source intended for building other packages which
use the "serde" feature of the "%{crate}" crate.

%files       -n %{name}+serde-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+v3-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+v3-devel %{_description}

This package contains library source intended for building other packages which
use the "v3" feature of the "%{crate}" crate.

%files       -n %{name}+v3-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+v4-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+v4-devel %{_description}

This package contains library source intended for building other packages which
use the "v4" feature of the "%{crate}" crate.

%files       -n %{name}+v4-devel
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