# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate nu-cli

Name:           rust-nu-cli
Version:        0.96.1
Release:        %autorelease
Summary:        CLI-related functionality for Nushell

License:        MIT
URL:            https://crates.io/crates/nu-cli
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
CLI-related functionality for Nushell.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
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

%package     -n %{name}+nu-plugin-engine-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+nu-plugin-engine-devel %{_description}

This package contains library source intended for building other packages which
use the "nu-plugin-engine" feature of the "%{crate}" crate.

%files       -n %{name}+nu-plugin-engine-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+plugin-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+plugin-devel %{_description}

This package contains library source intended for building other packages which
use the "plugin" feature of the "%{crate}" crate.

%files       -n %{name}+plugin-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+system-clipboard-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+system-clipboard-devel %{_description}

This package contains library source intended for building other packages which
use the "system-clipboard" feature of the "%{crate}" crate.

%files       -n %{name}+system-clipboard-devel
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
# * other tests depend on unshipped fixtures
%cargo_test -- --lib
%endif

%changelog
%autochangelog