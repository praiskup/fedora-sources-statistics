# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate salsa20

Name:           rust-salsa20
Version:        0.10.2
Release:        %autorelease
Summary:        Salsa20 Stream Cipher

License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/salsa20
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Salsa20 Stream Cipher.}

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

%package     -n %{name}+std-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+std-devel %{_description}

This package contains library source intended for building other packages which
use the "std" feature of the "%{crate}" crate.

%files       -n %{name}+std-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+zeroize-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+zeroize-devel %{_description}

This package contains library source intended for building other packages which
use the "zeroize" feature of the "%{crate}" crate.

%files       -n %{name}+zeroize-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
# remove executable bit from non-executable source files
find -name "*.rs" -executable -print -exec chmod -x {} +
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