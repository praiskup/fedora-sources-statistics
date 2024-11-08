%global upstreamname rocSOLVER
%global rocm_release 6.2
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
# build_cxxflags does not honor CMAKE_BUILD_TYPE, strip out -g
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-g / /')

# $gpu will be evaluated in the loops below
%global _vpath_builddir %{_vendor}-%{_target_os}-build-${gpu}

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RELEASE
%global debug_package %{nil}
%endif

%bcond_without compress
%if %{with compress}
%global build_compress ON
%else
%global build_compress OFF
%endif

%bcond_with test
%if %{with test}
%global build_test ON
%global __brp_check_rpaths %{nil}
%else
%global build_test OFF
%endif

# may run out of memory for both compile and link
# Use fine tuned cmake ROCSOLVER_PARALLEL_COMPILE|LINK_JOBS switches
%global _smp_mflags %{nil}

# Fortran is only used in testing
%global build_fflags %{nil}

Name:           rocsolver
Version:        %{rocm_version}
Release:        %autorelease
Summary:        Next generation LAPACK implementation for ROCm platform
Url:            https://github.com/ROCm/rocSOLVER

# License check reports BSD 2-Clause
# But reviewing LICENSE.md, this is only for AMD
# Later in the file are BSD 3-Clause for LAPACK and MAGMA
License:        BSD-3-Clause AND BSD-2-Clause

# Only x86_64 works right now:
ExclusiveArch:  x86_64

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
# https://github.com/ROCm/rocSOLVER/pull/652
Patch0:         0001-Add-llvm-style-compile-and-link-options.patch
Patch1:         0001-rocsolver-offload-compress.patch

BuildRequires:  cmake
BuildRequires:  fmt-devel
BuildRequires:  ninja-build
BuildRequires:  rocblas-devel
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpm-macros-modules
BuildRequires:  rocprim-devel
BuildRequires:  rocsparse-devel

%if %{with compress}
BuildRequires:  pkgconfig(libzstd)
%endif

%if %{with test}
BuildRequires:  blas-static
BuildRequires:  gcc-gfortran
BuildRequires:  gtest-devel
BuildRequires:  lapack-static
%endif

%description
rocSOLVER is a work-in-progress implementation of a subset
of LAPACK functionality on the ROCm platform.

%package devel
Summary: Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

%build

# Real cores, No hyperthreading
COMPILE_JOBS=`cat /proc/cpuinfo | grep -m 1 'cpu cores' | awk '{ print $4 }'`
if [ ${COMPILE_JOBS}x = x ]; then
    COMPILE_JOBS=1
fi
# Take into account memmory usage per core, do not thrash real memory
BUILD_MEM=4
MEM_KB=0
MEM_KB=`cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'`
MEM_MB=`eval "expr ${MEM_KB} / 1024"`
MEM_GB=`eval "expr ${MEM_MB} / 1024"`
COMPILE_JOBS_MEM=`eval "expr 1 + ${MEM_GB} / ${BUILD_MEM}"`
if [ "$COMPILE_JOBS_MEM" -lt "$COMPILE_JOBS" ]; then
    COMPILE_JOBS=$COMPILE_JOBS_MEM
fi
LINK_MEM=32
LINK_JOBS=`eval "expr 1 + ${MEM_GB} / ${LINK_MEM}"`

for gpu in %{rocm_gpu_list}
do
    module load rocm/$gpu
    %cmake -G Ninja \
           -DCMAKE_BUILD_TYPE=%{build_type} \
	   -DCMAKE_SKIP_RPATH=ON \
	   -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
	   -DROCM_SYMLINK_LIBS=OFF \
	   -DHIP_PLATFORM=amd \
	   -DAMDGPU_TARGETS=$ROCM_GPUS \
	   -DCMAKE_INSTALL_LIBDIR=$ROCM_LIB \
	   -DCMAKE_INSTALL_BINDIR=$ROCM_BIN \
           -DROCSOLVER_PARALLEL_COMPILE_JOBS=$COMPILE_JOBS \
           -DROCSOLVER_PARALLEL_LINK_JOBS=$LINK_JOBS \
	   -DBUILD_OFFLOAD_COMPRESS=%{build_compress} \
           -DBUILD_CLIENTS_TESTS=%{build_test}

    %cmake_build
    module purge
done

%install
for gpu in %{rocm_gpu_list}
do
    %cmake_install
done

echo s@%{buildroot}@@ > br.sed
find %{buildroot}%{_libdir} -name '*.so.*.[0-9]' | sed -f br.sed >  %{name}.files
find %{buildroot}%{_libdir} -name '*.so.[0-9]'   | sed -f br.sed >> %{name}.files
find %{buildroot}%{_libdir} -name '*.so'         | sed -f br.sed >  %{name}.devel
find %{buildroot}%{_libdir} -name '*.cmake'      | sed -f br.sed >> %{name}.devel
%if %{with test}
find %{buildroot}           -name '%{name}-*'    | sed -f br.sed >  %{name}.test
find %{buildroot}           -name 'mat_*'        | sed -f br.sed >> %{name}.test
find %{buildroot}           -name 'posmat_*'     | sed -f br.sed >> %{name}.test
%endif

%files -f %{name}.files
%license LICENSE.md
%exclude %{_docdir}/%{name}/LICENSE.md

%files devel -f %{name}.devel
%doc README.md
%{_includedir}/%{name}/*.h

%if %{with test}
%files test -f %{name}.test
%endif

%changelog
%autochangelog
