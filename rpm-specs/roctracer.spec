%global upstreamname roctracer
%global rocm_release 6.2
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain clang
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')

# Needs ROCm HW and is only suitable for local testing
%bcond_with test
%if %{with test}
# rpm flags interfere with building the tests
%global build_cflags %{nil}
%endif

%bcond_with doc

Name:           roctracer
Version:        %{rocm_version}
Release:        %autorelease
Summary:        ROCm Tracer Callback/Activity Library for Performance tracing AMD GPUs

Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT
Source0:        %{url}/archive/refs/tags/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  clang-devel
BuildRequires:  compiler-rt
BuildRequires:  libatomic
BuildRequires:  lld
BuildRequires:  llvm-devel
BuildRequires:  ninja-build
BuildRequires:  python-cppheaderparser
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
%if %{with doc}
BuildRequires:  doxygen
BuildRequires:  texlive-adjustbox
BuildRequires:  texlive-dvips
BuildRequires:  texlive-ec
BuildRequires:  texlive-hanging
BuildRequires:  texlive-latex
BuildRequires:  texlive-makeindex
BuildRequires:  texlive-metafont
BuildRequires:  texlive-multirow
BuildRequires:  texlive-newunicodechar
BuildRequires:  texlive-stackengine
BuildRequires:  texlive-texlive-scripts
BuildRequires:  texlive-tocloft
BuildRequires:  texlive-ulem
BuildRequires:  texlive-url
BuildRequires:  texlive-wasy
BuildRequires:  texlive-wasysym
%endif

# ROCm is only x86_64 for now
ExclusiveArch:  x86_64

%description
ROC-tracer

* ROC-tracer library: Runtimes Generic Callback/Activity APIs

  The goal of the implementation is to provide a generic independent
  from specific runtime profiler to trace API and asynchronous activity.

  The API provides functionality for registering the runtimes API
  callbacks and asynchronous activity records pool support.

* ROC-TX library: Code Annotation Events API

  Includes API for:

  * roctxMark
  * roctxRangePush
  * roctxRangePop

%package devel
Summary:        The %{name} development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The headers of libraries for %{name}.

%if %{with doc}
%package doc
Summary:        Docs for %{name}

%description doc
%{summary}
%endif

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

# No knob in cmake to turn off testing
%if %{without test}
sed -i -e 's@add_subdirectory(test)@#add_subdirectory(test)@' CMakeLists.txt
%endif

%build
%cmake -G Ninja \
       -DCMAKE_MODULE_PATH=%{_libdir}/cmake/hip \
       -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
       -DROCM_SYMLINK_LIBS=OFF \
       -DHIP_PLATFORM=amd \
       -DBUILD_SHARED_LIBS=ON \
       -DAMDGPU_TARGETS=$ROCM_GPUS \
       -DCMAKE_BUILD_TYPE=RelDebInfo

%cmake_build

%if %{with doc}
%cmake_build -t doc
%endif

%install
%cmake_install

# Only install the pdf
rm -rf rm %{buildroot}%{_datadir}/html

%files
%dir %{_libdir}/%{name}
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}64.so.*
%{_libdir}/libroctx64.so.*
%{_libdir}/%{name}/libfile_plugin.so
%{_libdir}/%{name}/libhip_stats.so
%{_libdir}/%{name}/libroctracer_tool.so
%exclude %{_docdir}/%{name}*/LICENSE

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}64.so
%{_libdir}/libroctx64.so

%if %{with doc}
%files doc
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/%{name}.pdf
%endif

%if %{with test}
%files test
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%endif

%changelog
%autochangelog
