#Image support is x86 only
%ifarch x86_64
%global enableimage 1
%endif
%global rocm_release 6.2
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

Name:       rocm-runtime
Version:    %{rocm_version}
%if 0%{?rhel} && 0%{?rhel} < 10
Release:    1%{?dist}
%else
Release:    %autorelease
%endif
Summary:    ROCm Runtime Library

License:    NCSA
URL:        https://github.com/ROCm/ROCR-Runtime
Source0:    %{url}/archive/rocm-%{version}.tar.gz#/%{name}-%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  hipcc
BuildRequires:  hsakmt-devel
BuildRequires:  hsakmt(rocm) = %{rocm_release}
BuildRequires:  libdrm-devel
BuildRequires:  libffi-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-device-libs
BuildRequires:  vim-common

%description
The ROCm Runtime Library is a thin, user-mode API that exposes the necessary
interfaces to access and interact with graphics hardware driven by the AMDGPU
driver set and the AMDKFD kernel driver. Together they enable programmers to
directly harness the power of AMD discrete graphics devices by allowing host
applications to launch compute kernels directly to the graphics hardware.

%package devel
Summary: ROCm Runtime development files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: hsakmt(rocm) = %{rocm_release}

%description devel
ROCm Runtime development files


%prep
%autosetup -n ROCR-Runtime-rocm-%{version} -p1

%build

%cmake -S src -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DINCLUDE_PATH_COMPATIBILITY=OFF \
    %{?!enableimage:-DIMAGE_SUPPORT=OFF}
%cmake_build


%install
%cmake_install

%ldconfig_scriptlets

%files
%doc README.md
%license LICENSE.txt
%{_libdir}/libhsa-runtime64.so.1{,.*}
%exclude %{_docdir}/hsa-runtime64/LICENSE.md

%files devel
%{_includedir}/hsa/
%{_libdir}/libhsa-runtime64.so
%{_libdir}/cmake/hsa-runtime64/

%changelog
%autochangelog
