# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate enquote

Name:           rust-enquote
Version:        1.1.0
Release:        %autorelease
Summary:        Quotes and unquotes strings

License:        Unlicense
URL:            https://crates.io/crates/enquote
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Quotes and unquotes strings.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%doc %{crate_instdir}/readme.md
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
