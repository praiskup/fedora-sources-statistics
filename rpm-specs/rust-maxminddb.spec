# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate maxminddb

%global testdata_commit a8ae5b4ac0aa730e2783f708cdaa208aca20e9ec
%global testdata_short  %(c=%{testdata_commit}; echo ${c:0:7})

Name:           rust-maxminddb
Version:        0.23.0
Release:        %autorelease
Summary:        Library for reading MaxMind DB format used by GeoIP2 and GeoLite2

License:        ISC
URL:            https://crates.io/crates/maxminddb
Source0:        %{crates_source}
Source1:        https://github.com/maxmind/MaxMind-DB/archive/%{testdata_commit}/test-data-%{testdata_short}.tar.gz
# Manually created patch for downstream crate metadata changes
# * bump ipnetwork dependency from 0.18 to 0.20
# * drop unused, benchmark-only criterion dev-dependency to speed up builds
Patch:          maxminddb-fix-metadata.diff

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Library for reading MaxMind DB format used by GeoIP2 and GeoLite2.}

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

%package     -n %{name}+memmap2-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+memmap2-devel %{_description}

This package contains library source intended for building other packages which
use the "memmap2" feature of the "%{crate}" crate.

%files       -n %{name}+memmap2-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+mmap-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+mmap-devel %{_description}

This package contains library source intended for building other packages which
use the "mmap" feature of the "%{crate}" crate.

%files       -n %{name}+mmap-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+unsafe-str-decode-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unsafe-str-decode-devel %{_description}

This package contains library source intended for building other packages which
use the "unsafe-str-decode" feature of the "%{crate}" crate.

%files       -n %{name}+unsafe-str-decode-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1 -a1
mv MaxMind-DB-%{testdata_commit} test-data
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