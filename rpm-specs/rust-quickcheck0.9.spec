# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate quickcheck

Name:           rust-quickcheck0.9
Version:        0.9.2
Release:        %autorelease
Summary:        Automatic property based testing with shrinking

# Upstream license specification: Unlicense/MIT
License:        Unlicense OR MIT
URL:            https://crates.io/crates/quickcheck
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * bump env_logger dependency from 0.7 to 0.8
Patch:          quickcheck-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Automatic property based testing with shrinking.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/COPYING
%license %{crate_instdir}/LICENSE-MIT
%license %{crate_instdir}/UNLICENSE
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

%package     -n %{name}+env_logger-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+env_logger-devel %{_description}

This package contains library source intended for building other packages which
use the "env_logger" feature of the "%{crate}" crate.

%files       -n %{name}+env_logger-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+log-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+log-devel %{_description}

This package contains library source intended for building other packages which
use the "log" feature of the "%{crate}" crate.

%files       -n %{name}+log-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+regex-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+regex-devel %{_description}

This package contains library source intended for building other packages which
use the "regex" feature of the "%{crate}" crate.

%files       -n %{name}+regex-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+unstable-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unstable-devel %{_description}

This package contains library source intended for building other packages which
use the "unstable" feature of the "%{crate}" crate.

%files       -n %{name}+unstable-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+use_logging-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+use_logging-devel %{_description}

This package contains library source intended for building other packages which
use the "use_logging" feature of the "%{crate}" crate.

%files       -n %{name}+use_logging-devel
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