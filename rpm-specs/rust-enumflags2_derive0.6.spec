# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate enumflags2_derive

Name:           rust-enumflags2_derive0.6
Version:        0.6.4
Release:        %autorelease
Summary:        Implementation detail of the enumflags2 crate

License:        MIT OR Apache-2.0
URL:            https://crates.io/crates/enumflags2_derive
Source0:        %{crates_source}
# https://github.com/meithecatte/enumflags2/issues/45
Source1:        https://github.com/meithecatte/enumflags2/raw/v%{version}/enumflags/LICENSE-APACHE
Source2:        https://github.com/meithecatte/enumflags2/raw/v%{version}/enumflags/LICENSE-MIT

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Do not use directly, use the reexport in the `enumflags2` crate. This
allows for better compatibility across versions.}

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
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+not_literal-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+not_literal-devel %{_description}

This package contains library source intended for building other packages which
use the "not_literal" feature of the "%{crate}" crate.

%files       -n %{name}+not_literal-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep
cp -pav %{SOURCE1} %{SOURCE2} .

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