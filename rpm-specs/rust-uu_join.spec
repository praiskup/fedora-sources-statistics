# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

# prevent executables from being installed
%global cargo_install_bin 0

%global crate uu_join

Name:           rust-uu_join
Version:        0.0.27
Release:        %autorelease
Summary:        join ~ (uutils) merge lines from inputs with matching join fields

License:        MIT
URL:            https://crates.io/crates/uu_join
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 26

%global _description %{expand:
join ~ (uutils) merge lines from inputs with matching join fields.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%doc %{crate_instdir}/BENCHMARKING.md
%doc %{crate_instdir}/join.md
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