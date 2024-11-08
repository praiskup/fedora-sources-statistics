%if 0%{?fedora} || 0%{?rhel} >= 7
%global _docdir_fmt %{name}
%endif

Name: mbedtls3.6
Version: 3.6.2
Release: 1%{?dist}
Summary: Light-weight cryptographic and SSL/TLS library
# Note: The BSD Clause is for configs/ext/crypto_config_profile_medium.h is relicensed
# per https://github.com/Mbed-TLS/mbedtls/blob/development/configs/ext/README.md under
# the dual license below.
License: Apache-2.0 OR GPL-2.0-or-later
URL: https://www.trustedfirmware.org/projects/mbed-tls
Source0: https://github.com/Mbed-TLS/mbedtls/releases/download/mbedtls-%{version}/mbedtls-%{version}.tar.bz2
Patch0: 0001-mbedtls_xor-simplify-and-fix-build-error.diff
Patch1: 0002-mbedtls-suffix-with-version-upstream-not-stable.diff
Patch2: 0003-mbedtls-suffix-pkgconfig.diff
Patch3: 0004-3rd-party-static.diff
Patch4: 0005-no-install-static-libs.diff
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: perl-interpreter
BuildRequires: python3

%description
Mbed TLS is a light-weight open source cryptographic and SSL/TLS
library written in C. Mbed TLS makes it easy for developers to include
cryptographic and SSL/TLS capabilities in their (embedded)
applications with as little hassle as possible.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains documentation.

%prep
%autosetup -n mbedtls-%{version} -p1

sed -i 's|//\(#define MBEDTLS_THREADING_C\)|\1|' include/mbedtls/mbedtls_config.h
sed -i 's|//\(#define MBEDTLS_THREADING_PTHREAD\)|\1|' include/mbedtls/mbedtls_config.h

%build
export CFLAGS="%{optflags} -Wno-stringop-overflow -Wno-maybe-uninitialized"
export CXXLAGS="%{optflags} -Wno-stringop-overflow -Wno-maybe-uninitialized"

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DLINK_WITH_PTHREAD=ON \
    -DINSTALL_MBEDTLS_HEADERS=ON \
    -DENABLE_PROGRAMS=OFF \
    -DUSE_SHARED_MBEDTLS_LIBRARY=ON \
    -DUSE_STATIC_MBEDTLS_LIBRARY=OFF \
    -DGEN_FILES=OFF

%cmake_build
make apidoc

%install
%cmake_install

# Library files aren't supposed to be executable, but RPM requires this historically
# for automatic per-file level automatic dependency generation at ELF binaries; see:
# - https://github.com/ARMmbed/mbedtls/commit/280165c9b39091c7c7ffe031430c7cf93ebc4dec
# - https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/PDD6RNQMII472HXM4XAUUWWZKKBGHPTO/
chmod 755 %{buildroot}%{_libdir}/*.so.*

# We want to prefix all the files under their own include directories so mbedtls and mbedtls3.6, mbedtls-3.7,
# and so forth can be installed side by side. This is because of an unstable upstrem
mkdir -p %{buildroot}/%{_includedir}/mbedtls3.6
mv %{buildroot}/%{_includedir}/mbedtls %{buildroot}/%{_includedir}/mbedtls3.6

mkdir -p %{buildroot}/%{_includedir}/psa3.6
mv %{buildroot}/%{_includedir}/psa %{buildroot}/%{_includedir}/psa3.6

mkdir -p %{buildroot}/%{_includedir}/everest3.6
mv %{buildroot}/%{_includedir}/everest %{buildroot}/%{_includedir}/everest3.6

mv %{buildroot}/%{_libdir}/cmake/MbedTLS %{buildroot}/%{_libdir}/cmake/MbedTLS3.6

# They do file system stuff with the same file, so parallel file modifications
# cause testsuite failures.
%check
%ctest --output-on-failure --force-new-ctest-process --parallel 1

%files
%doc ChangeLog
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libmbedcrypto3.6.so.%{version}
%{_libdir}/libmbedtls3.6.so.%{version}
%{_libdir}/libmbedx5093.6.so.%{version}
%{_libdir}/libmbedcrypto3.6.so.16
%{_libdir}/libmbedtls3.6.so.21
%{_libdir}/libmbedx5093.6.so.7

%files devel
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_includedir}/mbedtls3.6/
%{_includedir}/psa3.6/
%{_includedir}/everest3.6/
%{_libdir}/pkgconfig/
%{_libdir}/cmake/
%{_libdir}/libmbedcrypto3.6.so
%{_libdir}/libmbedtls3.6.so
%{_libdir}/libmbedx5093.6.so

%files doc
%license LICENSE
%doc apidoc/*

%changelog
* Tue Oct 15 2024 Morten Stevens <mstevens@fedoraproject.org> - 3.6.2-1
- Update to 3.6.2

* Fri Sep 06 2024 Bill Roberts <bill.roberts@arm.com> - 3.6.1-1
- Update to 3.6.1
  - Notably Fixes CVE-2024-45157

* Tue Apr 02 2024 Bill Roberts <bill.roberts@arm.com> - 3.6.0-1
- Update to 3.6.0
