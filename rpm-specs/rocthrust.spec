%global upstreamname rocThrust

%global rocm_release 6.2
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

# Compiler is hipcc, which is clang based:
%global toolchain clang
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')
# there is no debug package
%global debug_package %{nil}

# Option to test suite for testing on real HW:
%bcond_with check

Name:           rocthrust
Version:        %{rocm_version}
Release:        %autorelease
Summary:        ROCm Thrust libary

Url:            https://github.com/ROCm
License:        Apache-2.0 and BSD-2-Clause and BSD-3-Clause and MIT and Public Domain
# All files are Apache 2.0 with some exceptions:
# ./cmake contains only files under MIT
# ./internal/benchmark/*.py are dual licensed Apache 2.0 and Boost 1.0
# ./thrust/ contain some headers files that are Boost 1.0 licensed
# ./thrust/ contain some headers that are dual Apache 2.0 and Boost 1.0
# ./thrust/cmake/FindTBB.cmake is public domain
# ./thrust/detail/allocator/allocator_traits.h is dual Apache 2.0 and MIT
# ./thrust/detail/complex contains BSD 2 clause licensed headers

Source0:        %{url}/%{upstreamname}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

BuildRequires:  cmake
%if %{with check}
BuildRequires:  gtest-devel
%endif
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocprim-static
BuildRequires:  rocm-runtime-devel

# Only headers, cmake infra, noarch confuses libdir
# BuildArch: noarch
# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
Thrust is a parallel algorithm library. This library has been
ported to HIP/ROCm platform, which uses the rocPRIM library.

%package devel
Summary:        The %{upstreamname} development package
Provides:       %{name}-static = %{version}-%{release}

%description devel
The %{upstreamname} development package.

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

#
# The ROCMExportTargetsHeaderOnly.cmake file
# generates a files that reference the install location of other files
# Make this change so they match
sed -i -e 's/ROCM_INSTALL_LIBDIR lib/ROCM_INSTALL_LIBDIR lib64/' cmake/ROCMExportTargetsHeaderOnly.cmake

%build
%cmake \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
%if %{with check}
    -DBUILD_TEST=ON \
%endif
    -DCMAKE_CXX_COMPILER=hipcc \
    -DROCM_SYMLINK_LIBS=OFF
%cmake_build

%install
%cmake_install

%check
%if %{with check}
%ctest
%endif

%files devel
%dir %{_docdir}/%{name}/
%doc README.md
%license %{_docdir}/%{name}/LICENSE
%license NOTICES.txt
%{_includedir}/thrust
%{_libdir}/cmake/%{name}

%changelog
%autochangelog
