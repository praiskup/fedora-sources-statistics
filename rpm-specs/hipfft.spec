%global upstreamname hipFFT
%global rocm_release 6.2
%global rocm_patch 1
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
%else
%global build_test OFF
%endif

Name:           hipfft
Version:        %{rocm_version}
Release:        %autorelease
Summary:        ROCm FFT marshalling library
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT

# Only x86_64 works right now
ExclusiveArch:  x86_64

Source0:        %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-rocm-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocprim-devel
BuildRequires:  rocfft-devel

%if %{with test}
BuildRequires:  boost-devel
BuildRequires:  fftw-devel
BuildRequires:  gtest-devel
BuildRequires:  hiprand-devel
BuildRequires:  libomp-devel
BuildRequires:  rocrand-devel
%endif

%description
hipFFT is an FFT marshalling library. Currently, hipFFT supports
the rocFFT backends

hipFFT exports an interface that does not require the client to
change, regardless of the chosen backend. It sits between the
application and the backend FFT library, marshalling inputs into
the backend and results back to the application.

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
%autosetup -n %{upstreamname}-rocm-%{version} -p 1

%build
for gpu in %{rocm_gpu_list}
do
    module load rocm/$gpu

    %cmake -G Ninja \
           -DCMAKE_BUILD_TYPE=%{build_type} \
	   -DCMAKE_SKIP_RPATH=ON \
	   -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
	   -DAMDGPU_TARGETS=${ROCM_GPUS} \
	   -DCMAKE_INSTALL_LIBDIR=$ROCM_LIB \
	   -DCMAKE_INSTALL_BINDIR=$ROCM_BIN \
           -DBUILD_CLIENTS_TESTS=%{build_test} \
	   -DROCM_SYMLINK_LIBS=OFF \
           -DHIP_PLATFORM=amd

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
%endif

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


