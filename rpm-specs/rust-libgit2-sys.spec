# Generated by rust2rpm 26
%bcond_without check
%global debug_package %{nil}

%global crate libgit2-sys
%global upstream_version 0.17.0+1.8.1

Name:           rust-libgit2-sys
Version:        0.17.0
Release:        %autorelease
Summary:        Native bindings to the libgit2 library

# * libgit2-sys crate:      MIT OR Apache-2.0
# * bundled libgit2:        GPL-2.0-only WITH GCC-exception-2.0
# * bundled llhttp:         MIT
# * bundled pcre:           BSD-3-Clause
License:        (MIT OR Apache-2.0) AND BSD-3-Clause AND GPL-2.0-only WITH GCC-exception-2.0 AND MIT
URL:            https://crates.io/crates/libgit2-sys
Source:         %{crates_source %{crate} %{upstream_version}}
# Automatically generated patch to strip dependencies and normalize metadata
Patch:          libgit2-sys-fix-metadata-auto.diff
# Manually created patch for downstream crate metadata changes
# * update package.license field to reflect bundled dependencies
# * drop features for statically linking against vendored OpenSSL
Patch:          libgit2-sys-fix-metadata.diff
# * build against the bundled copy of libgit2 unconditionally:
#   the version in the Fedora repositories is always either too old or too new
Patch:          0001-build-with-vendored-libgit2-unconditionally.patch

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Native bindings to the libgit2 library.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

Provides:       bundled(libgit2) = 1.8.1
Provides:       bundled(llhttp) = 9.2.1
Provides:       bundled(pcre) = 8.45

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-APACHE
%license %{crate_instdir}/LICENSE-MIT
%license %{crate_instdir}/libgit2/COPYING
%license %{crate_instdir}/libgit2/deps/llhttp/LICENSE-MIT
%license %{crate_instdir}/libgit2/deps/pcre/LICENCE
%doc %{crate_instdir}/CHANGELOG.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+https-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+https-devel %{_description}

This package contains library source intended for building other packages which
use the "https" feature of the "%{crate}" crate.

%files       -n %{name}+https-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+libssh2-sys-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+libssh2-sys-devel %{_description}

This package contains library source intended for building other packages which
use the "libssh2-sys" feature of the "%{crate}" crate.

%files       -n %{name}+libssh2-sys-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+openssl-sys-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+openssl-sys-devel %{_description}

This package contains library source intended for building other packages which
use the "openssl-sys" feature of the "%{crate}" crate.

%files       -n %{name}+openssl-sys-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+ssh-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+ssh-devel %{_description}

This package contains library source intended for building other packages which
use the "ssh" feature of the "%{crate}" crate.

%files       -n %{name}+ssh-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+ssh_key_from_memory-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+ssh_key_from_memory-devel %{_description}

This package contains library source intended for building other packages which
use the "ssh_key_from_memory" feature of the "%{crate}" crate.

%files       -n %{name}+ssh_key_from_memory-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+vendored-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+vendored-devel %{_description}

This package contains library source intended for building other packages which
use the "vendored" feature of the "%{crate}" crate.

%files       -n %{name}+vendored-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{upstream_version} -p1
# remove upstream development scripts from libgit2
rm -r libgit2/script/
# remove unused bundled dependencies
rm -r libgit2/deps/chromium-zlib
rm -r libgit2/deps/ntlmclient
rm -r libgit2/deps/winhttp
rm -r libgit2/deps/zlib
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