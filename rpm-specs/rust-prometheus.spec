# Generated by rust2rpm 23
%bcond_without check
%global debug_package %{nil}

%global crate prometheus

Name:           rust-prometheus
Version:        0.13.3
Release:        %autorelease
Summary:        Prometheus instrumentation library for Rust applications

License:        Apache-2.0
URL:            https://crates.io/crates/prometheus
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * drop unused, benchmark-only criterion dev-dependency to speed up builds
Patch:          prometheus-fix-metadata.diff

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Prometheus instrumentation library for Rust applications.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%doc %{crate_instdir}/CHANGELOG.md
%doc %{crate_instdir}/CODE_OF_CONDUCT.md
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

%package     -n %{name}+gen-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+gen-devel %{_description}

This package contains library source intended for building other packages which
use the "gen" feature of the "%{crate}" crate.

%files       -n %{name}+gen-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+libc-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+libc-devel %{_description}

This package contains library source intended for building other packages which
use the "libc" feature of the "%{crate}" crate.

%files       -n %{name}+libc-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+nightly-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+nightly-devel %{_description}

This package contains library source intended for building other packages which
use the "nightly" feature of the "%{crate}" crate.

%files       -n %{name}+nightly-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+process-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+process-devel %{_description}

This package contains library source intended for building other packages which
use the "process" feature of the "%{crate}" crate.

%files       -n %{name}+process-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+procfs-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+procfs-devel %{_description}

This package contains library source intended for building other packages which
use the "procfs" feature of the "%{crate}" crate.

%files       -n %{name}+procfs-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+protobuf-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+protobuf-devel %{_description}

This package contains library source intended for building other packages which
use the "protobuf" feature of the "%{crate}" crate.

%files       -n %{name}+protobuf-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+protobuf-codegen-pure-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+protobuf-codegen-pure-devel %{_description}

This package contains library source intended for building other packages which
use the "protobuf-codegen-pure" feature of the "%{crate}" crate.

%files       -n %{name}+protobuf-codegen-pure-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+push-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+push-devel %{_description}

This package contains library source intended for building other packages which
use the "push" feature of the "%{crate}" crate.

%files       -n %{name}+push-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+reqwest-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+reqwest-devel %{_description}

This package contains library source intended for building other packages which
use the "reqwest" feature of the "%{crate}" crate.

%files       -n %{name}+reqwest-devel
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