# Generated by rust2rpm 26
# * missing dev-dependency: netlink-packet-audit
%bcond_with check
%global debug_package %{nil}

%global crate netlink-sys

Name:           rust-netlink-sys
Version:        0.8.6
Release:        %autorelease
Summary:        Netlink sockets, with optional integration with tokio

License:        MIT
URL:            https://crates.io/crates/netlink-sys
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Netlink sockets, with optional integration with tokio.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-MIT
%doc %{crate_instdir}/CHANGELOG
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

%package     -n %{name}+async-io-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+async-io-devel %{_description}

This package contains library source intended for building other packages which
use the "async-io" feature of the "%{crate}" crate.

%files       -n %{name}+async-io-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+futures-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+futures-devel %{_description}

This package contains library source intended for building other packages which
use the "futures" feature of the "%{crate}" crate.

%files       -n %{name}+futures-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+mio-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+mio-devel %{_description}

This package contains library source intended for building other packages which
use the "mio" feature of the "%{crate}" crate.

%files       -n %{name}+mio-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+mio_socket-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+mio_socket-devel %{_description}

This package contains library source intended for building other packages which
use the "mio_socket" feature of the "%{crate}" crate.

%files       -n %{name}+mio_socket-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+smol_socket-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+smol_socket-devel %{_description}

This package contains library source intended for building other packages which
use the "smol_socket" feature of the "%{crate}" crate.

%files       -n %{name}+smol_socket-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+tokio-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+tokio-devel %{_description}

This package contains library source intended for building other packages which
use the "tokio" feature of the "%{crate}" crate.

%files       -n %{name}+tokio-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+tokio_socket-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+tokio_socket-devel %{_description}

This package contains library source intended for building other packages which
use the "tokio_socket" feature of the "%{crate}" crate.

%files       -n %{name}+tokio_socket-devel
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