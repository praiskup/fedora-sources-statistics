# libkrun tests require access to "/dev/kvm", which is usually not be available
# on build sandboxes.
%bcond_with check

Name:           libkrun
Version:        1.9.5
Release:        2%{?dist}
Summary:        Dynamic library providing Virtualization-based process isolation capabilities

License:        Apache-2.0
URL:            https://github.com/containers/libkrun
Source:         https://github.com/containers/libkrun/archive/refs/tags/v%{version}.tar.gz
# Generated with:
#  cargo vendor-filterer --platform=*-unknown-linux-gnu --features blk,net,gpu,snd,amd-sev
Source1:        %{name}-%{version}-vendor.tar.xz

# libkrun only supports x86_64 and aarch64
ExclusiveArch:  x86_64 aarch64

# While this project is composed mostly of Rust code, this is not a
# conventional Rust crate. The root of the project is a workspace, there's a C
# file that also needs to be compiled, and the resulting binary a dynamic
# library providing a C-compatible ABI.
#
# As a result, we can't fully rely on rust-packaging for managing this package.
# Instead, we use some of its tasks (cargo_prep and cargo_test) and combine
# them with using the Makefile provided by the project. We also need to manage
# BuildRequires manually, as rust-packaging gets confused trying to generate
# them dynamically.
BuildRequires:  rust-packaging >= 21
BuildRequires:  glibc-static
BuildRequires:  patchelf
BuildRequires:  binutils
BuildRequires:  libepoxy-devel
BuildRequires:  libdrm-devel
BuildRequires:  virglrenderer-devel
BuildRequires:  pipewire-devel
BuildRequires:  clang-devel
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  libkrunfw-devel >= 4.0.0
%ifarch x86_64
BuildRequires:  libkrunfw-sev-devel >= 4.0.0
%endif
%ifarch aarch64
BuildRequires:  libfdt-devel
%endif

%description
%{summary}.

%package devel
Summary: Header files and libraries for libkrun development
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The libkrun-devel package containes the libraries and headers needed to
develop programs that use libkrun Virtualization-based process isolation
capabilities.

# SEV is a feature provided by AMD EPYC processors, so only it's only
# available on x86_64.
%ifarch x86_64
%package sev
Summary: Dynamic library providing Virtualization-based process isolation capabilities (SEV variant)
BuildRequires:  libkrunfw-sev-devel >= 3.6.0

%description sev
Dynamic library providing Virtualization-based process isolation
capabilities, with the ability to use AMD SEV to create a microVM-based
Trusted Execution Environment (TEE).

%package sev-devel
Summary: Header files and libraries for libkrun development
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-sev%{?_isa} = %{version}-%{release}

%description sev-devel
The libkrun-sev-devel package containes the libraries and headers needed to
develop programs that use libkrun-sev Virtualization-based process isolation
capabilities.
%endif

%prep
%autosetup -n %{name}-%{version_no_tilde} -p1 -a1
%cargo_prep -v vendor

%build
%make_build init/init
%make_build libkrun.pc
%make_build GPU=1 BLK=1 NET=1 SND=1
patchelf --set-soname libkrun.so.1 --output target/release/libkrun.so.%{version} target/release/libkrun.so
%ifarch x86_64
    rm init/init
    %make_build SEV=1 init/init
    %cargo_build -f amd-sev
    mv target/release/libkrun.so target/release/libkrun-sev.so
    patchelf --set-soname libkrun-sev.so.1 --output target/release/libkrun-sev.so.%{version} target/release/libkrun-sev.so
%endif
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
%make_install PREFIX=%{_prefix}
%ifarch x86_64
    %make_install SEV=1 PREFIX=%{_prefix}
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_libdir}/libkrun.so.%{version}
%{_libdir}/libkrun.so.1

%files devel
%{_libdir}/libkrun.so
%{_libdir}/pkgconfig/libkrun.pc
%{_includedir}/libkrun.h

%ifarch x86_64
%files sev
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_libdir}/libkrun-sev.so.%{version}
%{_libdir}/libkrun-sev.so.1

%files sev-devel
%{_libdir}/libkrun-sev.so
%endif

%if %{with check}
%check
%cargo_test
%endif

%changelog
* Fri Sep 27 2024 Sergio Lopez <slp@redhat.com> - 1.9.5-1
- Update to version 1.9.5
- Vendorize dependencies ahead of package unification

* Tue Jul 23 2024 Sergio Lopez <slp@redhat.com> - 1.9.4-1
- Update to version 1.9.4

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 04 2024 Sergio Lopez <slp@redhat.com> - 1.9.2-1
- Update to version 1.9.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Sergio Lopez <slp@redhat.com> - 1.7.2-2
- Update versions of rust-vmm dependencies

* Sun Dec 24 2023 Sergio Lopez <slp@redhat.com> - 1.7.2-1
- Update to version 1.7.2

* Fri Dec 01 2023 Fabio Valentini <decathorpe@gmail.com> - 1.5.0-7
- Rebuild for openssl crate >= v0.10.60 (RUSTSEC-2023-0044, RUSTSEC-2023-0072)

* Tue Sep 19 2023 Fabio Valentini <decathorpe@gmail.com> - 1.5.0-6
- Rebuild for vm-memory v0.12.2 / CVE-2023-41051.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Sergio Lopez <slp@redhat.com> - 1.5.0-4
- Update license specification to conform SPDX format

* Wed Jul 19 2023 Sergio Lopez <slp@redhat.com> - 1.5.0-3
- Update vm-memory requirement to version 0.12.0
- Update kvm-ioctls requirement to version 0.14.0
- Add a temporary patch to accomodate an API change in kvm-ioctls

* Wed May 03 2023 Fabio Valentini <decathorpe@gmail.com> - 1.5.0-2
- Rebuild for openssl crate >= v0.10.48 (RUSTSEC-2023-{0022,0023,0024})

* Thu Feb 09 2023 Sergio Lopez <slp@redhat.com> - 1.5.0-1
- Update to version 1.5.0
- Update vm-memory, kvm-bindings, kvm-ioctls, vmm-sys-utils and sev
  dependencies
- Add a patch to update and relax vm-memory dependency

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov  8 2022 Sergio Lopez <slp@redhat.com> - 1.4.8-1
- Update to upstream version 1.4.8
- Add crossbeam-channel to the list of dependencies
- Update libkrun-remove-sev-deps.diff patch

* Fri Aug 26 2022 Cole Robinson <crobinso@redhat.com> - 1.4.2-2
- Allow building with rust-sev-0.3.0

* Wed Aug 17 2022 Sergio Lopez <slp@redhat.com> - 1.4.2-1
- Update to upstream version 1.4.2
- Add the libkrun-sev and libkrun-sev-devel subpackages with the SEV variant of
  the library.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Sergio Lopez <slp@redhat.com> - 1.2.2-1
- Initial package

