# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate uuid

Name:           rust-uuid0.7
Version:        0.7.4
Release:        %autorelease
Summary:        Library to generate and parse UUIDs

License:        Apache-2.0 OR MIT
URL:            https://crates.io/crates/uuid
Source:         %{crates_source}
# Automatically generated patch to strip foreign dependencies
Patch:          uuid-fix-metadata-auto.diff
# Manually created patch for downstream crate metadata changes
# * bump md5 dependency from 0.6 to 0.7:
#   https://github.com/uuid-rs/uuid/pull/442
# * drop Windows- and WASM-specific features
Patch:          uuid-fix-metadata.diff

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
A library to generate and parse UUIDs.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/COPYRIGHT
%license %{crate_instdir}/LICENSE-APACHE
%license %{crate_instdir}/LICENSE-MIT
%doc %{crate_instdir}/CODE_OF_CONDUCT.md
%doc %{crate_instdir}/CONTRIBUTING.md
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

%package     -n %{name}+byteorder-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+byteorder-devel %{_description}

This package contains library source intended for building other packages which
use the "byteorder" feature of the "%{crate}" crate.

%files       -n %{name}+byteorder-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+const_fn-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+const_fn-devel %{_description}

This package contains library source intended for building other packages which
use the "const_fn" feature of the "%{crate}" crate.

%files       -n %{name}+const_fn-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+md5-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+md5-devel %{_description}

This package contains library source intended for building other packages which
use the "md5" feature of the "%{crate}" crate.

%files       -n %{name}+md5-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+nightly-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+nightly-devel %{_description}

This package contains library source intended for building other packages which
use the "nightly" feature of the "%{crate}" crate.

%files       -n %{name}+nightly-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+rand-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+rand-devel %{_description}

This package contains library source intended for building other packages which
use the "rand" feature of the "%{crate}" crate.

%files       -n %{name}+rand-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+serde-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+serde-devel %{_description}

This package contains library source intended for building other packages which
use the "serde" feature of the "%{crate}" crate.

%files       -n %{name}+serde-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+sha1-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+sha1-devel %{_description}

This package contains library source intended for building other packages which
use the "sha1" feature of the "%{crate}" crate.

%files       -n %{name}+sha1-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+slog-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+slog-devel %{_description}

This package contains library source intended for building other packages which
use the "slog" feature of the "%{crate}" crate.

%files       -n %{name}+slog-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+std-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+std-devel %{_description}

This package contains library source intended for building other packages which
use the "std" feature of the "%{crate}" crate.

%files       -n %{name}+std-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+u128-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+u128-devel %{_description}

This package contains library source intended for building other packages which
use the "u128" feature of the "%{crate}" crate.

%files       -n %{name}+u128-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+v1-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+v1-devel %{_description}

This package contains library source intended for building other packages which
use the "v1" feature of the "%{crate}" crate.

%files       -n %{name}+v1-devel
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

%package     -n %{name}+v5-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+v5-devel %{_description}

This package contains library source intended for building other packages which
use the "v5" feature of the "%{crate}" crate.

%files       -n %{name}+v5-devel
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
