# Generated by rust2rpm 26
# * tests can only be run in-tree
%bcond_with check
%global debug_package %{nil}

%global crate tracing-futures

Name:           rust-tracing-futures
Version:        0.2.5
Release:        %autorelease
Summary:        Utilities for instrumenting futures with tracing

License:        MIT
URL:            https://crates.io/crates/tracing-futures
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * drop unused support for tokio ^0.1 and futures ^0.1
Patch:          tracing-futures-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Utilities for instrumenting `futures` with `tracing`.}

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

%package     -n %{name}+futures-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+futures-devel %{_description}

This package contains library source intended for building other packages which
use the "futures" feature of the "%{crate}" crate.

%files       -n %{name}+futures-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+futures-03-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+futures-03-devel %{_description}

This package contains library source intended for building other packages which
use the "futures-03" feature of the "%{crate}" crate.

%files       -n %{name}+futures-03-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+futures-task-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+futures-task-devel %{_description}

This package contains library source intended for building other packages which
use the "futures-task" feature of the "%{crate}" crate.

%files       -n %{name}+futures-task-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+pin-project-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+pin-project-devel %{_description}

This package contains library source intended for building other packages which
use the "pin-project" feature of the "%{crate}" crate.

%files       -n %{name}+pin-project-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+std-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+std-devel %{_description}

This package contains library source intended for building other packages which
use the "std" feature of the "%{crate}" crate.

%files       -n %{name}+std-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+std-future-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+std-future-devel %{_description}

This package contains library source intended for building other packages which
use the "std-future" feature of the "%{crate}" crate.

%files       -n %{name}+std-future-devel
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
