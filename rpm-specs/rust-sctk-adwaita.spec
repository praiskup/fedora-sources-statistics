# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate sctk-adwaita

Name:           rust-sctk-adwaita
Version:        0.10.1
Release:        %autorelease
Summary:        Adwaita-like SCTK Frame

License:        MIT
URL:            https://crates.io/crates/sctk-adwaita
Source:         %{crates_source}
# * Fedora patch: use system font instead of a bundled copy
Patch2:        sctk-adwaita-0.5.4-unbundle-cantarell-font.patch

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  abattis-cantarell-fonts

%global _description %{expand:
Adwaita-like SCTK Frame.}

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

%package     -n %{name}+ab_glyph-devel
Summary:        %{summary}
BuildArch:      noarch
Requires:       abattis-cantarell-fonts

%description -n %{name}+ab_glyph-devel %{_description}

This package contains library source intended for building other packages which
use the "ab_glyph" feature of the "%{crate}" crate.

%files       -n %{name}+ab_glyph-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+crossfont-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+crossfont-devel %{_description}

This package contains library source intended for building other packages which
use the "crossfont" feature of the "%{crate}" crate.

%files       -n %{name}+crossfont-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+memmap2-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+memmap2-devel %{_description}

This package contains library source intended for building other packages which
use the "memmap2" feature of the "%{crate}" crate.

%files       -n %{name}+memmap2-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep
# remove bundled fonts
rm -f src/title/*.ttf

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