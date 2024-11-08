%global upstreamname hipSOLVER
%global rocm_release 6.2
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')

# $gpu will be evaluated in the loops below             
%global _vpath_builddir %{_vendor}-%{_target_os}-build-${gpu}

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

%bcond_with test
%if %{with test}
%global build_test ON
%global __brp_check_rpaths %{nil}
# test parallel building broken
%global _smp_mflags -j1
%else
%global build_test OFF
%endif

# gfortran and clang rpm macros do not mix
%global build_fflags %{nil}

Name:           hipsolver
Version:        %{rocm_version}
Release:        %autorelease
Summary:        ROCm SOLVER marshalling library
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-gfortran
BuildRequires:  ninja-build
BuildRequires:  rocblas-devel
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpm-macros-modules
BuildRequires:  rocsolver-devel
BuildRequires:  rocsparse-devel
BuildRequires:  suitesparse-devel

%if %{with test}
BuildRequires:  blas-static
BuildRequires:  gtest-devel
BuildRequires:  hipsparse-devel
BuildRequires:  lapack-static
%endif

Requires:       rocm-rpm-macros-modules

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
hipSOLVER is a LAPACK marshalling library, with multiple supported
backends. It sits between the application and a 'worker'
LAPACK library, marshalling inputs into the backend library and
marshalling results back to the application. hipSOLVER exports an
interface that does not require the client to change, regardless
of the chosen backend. Currently, hipSOLVER supports rocSOLVER
and cuSOLVER as backends.

%package devel
Summary:        Libraries and headers for %{name}
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
find %{buildroot}           -name '%{name}-*'    | sed -f br.sed >  %{name}.test
find %{buildroot}           -name 'mat_*'        | sed -f br.sed >> %{name}.test
find %{buildroot}           -name 'posmat_*'     | sed -f br.sed >> %{name}.test

%files -f %{name}.files
%license LICENSE.md
%exclude %{_docdir}/%{name}/LICENSE.md

%files devel -f %{name}.devel
%doc README.md
%{_includedir}/%{name}

%if %{with test}
%files test -f %{name}.test
%endif

%changelog
%autochangelog
