# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate winnow

Name:           rust-winnow
Version:        0.6.20
Release:        %autorelease
Summary:        Byte-oriented, zero-copy, parser combinators library

License:        MIT
URL:            https://crates.io/crates/winnow
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * remove references to benchmark and example binaries from Cargo.toml
# * drop unused, benchmark-only criterion dev-dependency
# * drop dev-dependencies which are only needed for example binaries
Patch:          winnow-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
A byte-oriented, zero-copy, parser combinators library.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-MIT
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

%package     -n %{name}+alloc-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+alloc-devel %{_description}

This package contains library source intended for building other packages which
use the "alloc" feature of the "%{crate}" crate.

%files       -n %{name}+alloc-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+debug-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+debug-devel %{_description}

This package contains library source intended for building other packages which
use the "debug" feature of the "%{crate}" crate.

%files       -n %{name}+debug-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+simd-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+simd-devel %{_description}

This package contains library source intended for building other packages which
use the "simd" feature of the "%{crate}" crate.

%files       -n %{name}+simd-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+std-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+std-devel %{_description}

This package contains library source intended for building other packages which
use the "std" feature of the "%{crate}" crate.

%files       -n %{name}+std-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+unstable-doc-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unstable-doc-devel %{_description}

This package contains library source intended for building other packages which
use the "unstable-doc" feature of the "%{crate}" crate.

%files       -n %{name}+unstable-doc-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+unstable-recover-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unstable-recover-devel %{_description}

This package contains library source intended for building other packages which
use the "unstable-recover" feature of the "%{crate}" crate.

%files       -n %{name}+unstable-recover-devel
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