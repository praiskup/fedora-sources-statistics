# Generated by rust2rpm 26
# * examples and integration tests are not included in published crates
%bcond_with check
%global debug_package %{nil}

%global crate hyper

Name:           rust-hyper
Version:        1.5.0
Release:        %autorelease
Summary:        Fast and correct HTTP library

License:        MIT
URL:            https://crates.io/crates/hyper
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
A fast and correct HTTP library.}

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

%package     -n %{name}+client-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+client-devel %{_description}

This package contains library source intended for building other packages which
use the "client" feature of the "%{crate}" crate.

%files       -n %{name}+client-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+ffi-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+ffi-devel %{_description}

This package contains library source intended for building other packages which
use the "ffi" feature of the "%{crate}" crate.

%files       -n %{name}+ffi-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+full-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+full-devel %{_description}

This package contains library source intended for building other packages which
use the "full" feature of the "%{crate}" crate.

%files       -n %{name}+full-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+http1-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+http1-devel %{_description}

This package contains library source intended for building other packages which
use the "http1" feature of the "%{crate}" crate.

%files       -n %{name}+http1-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+http2-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+http2-devel %{_description}

This package contains library source intended for building other packages which
use the "http2" feature of the "%{crate}" crate.

%files       -n %{name}+http2-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+server-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+server-devel %{_description}

This package contains library source intended for building other packages which
use the "server" feature of the "%{crate}" crate.

%files       -n %{name}+server-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+tracing-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+tracing-devel %{_description}

This package contains library source intended for building other packages which
use the "tracing" feature of the "%{crate}" crate.

%files       -n %{name}+tracing-devel
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