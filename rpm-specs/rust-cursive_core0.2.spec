# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate cursive_core

Name:           rust-cursive_core0.2
Version:        0.2.2
Release:        %autorelease
Summary:        Core components for the Cursive TUI

License:        MIT
URL:            https://crates.io/crates/cursive_core
Source:         %{crates_source}
# PR to add license to the crates: https://github.com/gyscos/cursive/pull/702
Source1:        https://raw.githubusercontent.com/gyscos/cursive/main/LICENSE
# Manually created patch for downstream crate metadata changes
# - bump ahash to 0.7
# - bump enum-map to 1.1
Patch:          cursive_core-fix-metadata.diff
# * backported upstream patch to fix tests with unicode-width >= 0.1.13:
#   https://github.com/gyscos/cursive/commit/a0e405e
Patch:          0001-Make-spans-test-adaptable-to-unicode-width-version.patch

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Core components for the Cursive TUI.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%doc %{crate_instdir}/Readme.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+markdown-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+markdown-devel %{_description}

This package contains library source intended for building other packages which
use the "markdown" feature of the "%{crate}" crate.

%files       -n %{name}+markdown-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+pulldown-cmark-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+pulldown-cmark-devel %{_description}

This package contains library source intended for building other packages which
use the "pulldown-cmark" feature of the "%{crate}" crate.

%files       -n %{name}+pulldown-cmark-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+toml-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+toml-devel %{_description}

This package contains library source intended for building other packages which
use the "toml" feature of the "%{crate}" crate.

%files       -n %{name}+toml-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+unstable_scroll-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unstable_scroll-devel %{_description}

This package contains library source intended for building other packages which
use the "unstable_scroll" feature of the "%{crate}" crate.

%files       -n %{name}+unstable_scroll-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version} -p1
cp -p %{SOURCE1} .
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