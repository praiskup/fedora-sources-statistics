# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate google-cloud-metadata

Name:           rust-google-cloud-metadata
Version:        0.5.0
Release:        %autorelease
Summary:        Google Cloud Platform rust client

License:        MIT
URL:            https://crates.io/crates/google-cloud-metadata
Source0:         %{crates_source}

# license from GitHub repo
Source1:        https://raw.githubusercontent.com/yoshidan/google-cloud-rust/main/LICENSE

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Google Cloud Platform rust client.}

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

%prep
%autosetup -n %{crate}-%{version} -p1
cp %SOURCE1 .
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
