# Generated by rust2rpm 25
%bcond_without check
%global debug_package %{nil}

%global crate bindgen

Name:           rust-bindgen0.68
Version:        0.68.1
Release:        %autorelease
Summary:        Automatically generates Rust FFI bindings to C and C++ libraries

License:        BSD-3-Clause
URL:            https://crates.io/crates/bindgen
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Automatically generates Rust FFI bindings to C and C++ libraries.}

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

%package     -n %{name}+__cli-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+__cli-devel %{_description}

This package contains library source intended for building other packages which
use the "__cli" feature of the "%{crate}" crate.

%files       -n %{name}+__cli-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+__testing_only_extra_assertions-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+__testing_only_extra_assertions-devel %{_description}

This package contains library source intended for building other packages which
use the "__testing_only_extra_assertions" feature of the "%{crate}" crate.

%files       -n %{name}+__testing_only_extra_assertions-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+__testing_only_libclang_5-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+__testing_only_libclang_5-devel %{_description}

This package contains library source intended for building other packages which
use the "__testing_only_libclang_5" feature of the "%{crate}" crate.

%files       -n %{name}+__testing_only_libclang_5-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+__testing_only_libclang_9-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+__testing_only_libclang_9-devel %{_description}

This package contains library source intended for building other packages which
use the "__testing_only_libclang_9" feature of the "%{crate}" crate.

%files       -n %{name}+__testing_only_libclang_9-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+experimental-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+experimental-devel %{_description}

This package contains library source intended for building other packages which
use the "experimental" feature of the "%{crate}" crate.

%files       -n %{name}+experimental-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+logging-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+logging-devel %{_description}

This package contains library source intended for building other packages which
use the "logging" feature of the "%{crate}" crate.

%files       -n %{name}+logging-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+prettyplease-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+prettyplease-devel %{_description}

This package contains library source intended for building other packages which
use the "prettyplease" feature of the "%{crate}" crate.

%files       -n %{name}+prettyplease-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+runtime-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+runtime-devel %{_description}

This package contains library source intended for building other packages which
use the "runtime" feature of the "%{crate}" crate.

%files       -n %{name}+runtime-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+static-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+static-devel %{_description}

This package contains library source intended for building other packages which
use the "static" feature of the "%{crate}" crate.

%files       -n %{name}+static-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+which-rustfmt-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+which-rustfmt-devel %{_description}

This package contains library source intended for building other packages which
use the "which-rustfmt" feature of the "%{crate}" crate.

%files       -n %{name}+which-rustfmt-devel
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