%global upstreamname HIPIFY

%global rocm_release 6.2
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

# This is a clang tool so best to build with clang
%global toolchain clang

Name:           hipify
Version:        %{rocm_version}
Release:        %autorelease
Summary:        Convert CUDA to HIP

Url:            https://github.com/ROCm
License:        MIT
Source0:        %{url}/%{upstreamname}/archive/refs/tags/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz
Patch0:         0001-prepare-hipify-cmake-for-fedora.patch

BuildRequires:  cmake
# Hipify doesn't need hipcc, but this is the easiest way to pull in the same
# llvm/lld/clang/compiler-rt version as hipcc:
BuildRequires:  hipcc
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  perl
BuildRequires:  zlib-devel

Requires:       perl

# ROCm is really only on x86_64
ExclusiveArch:  x86_64

%description
HIPIFY is a set of tools to translate CUDA source code into portable
HIP C++ automatically.

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

%build

LLVM_CMAKEDIR=`llvm-config-%{rocmllvm_version} --cmakedir`
if [ ! -d ${LLVM_CMAKEDIR} ]; then
    echo "Something wrong with llvm-config"
    false
fi
LLVM_BINDIR=`llvm-config-%{rocmllvm_version} --bindir`
if [ ! -x ${LLVM_BINDIR}/clang ]; then
    echo "Something wrong with llvm-config"
    false
fi
export CC=${LLVM_BINDIR}/clang
export CXX=${LLVM_BINDIR}/clang

%cmake -DCMAKE_PREFIX_PATH=${LLVM_CMAKEDIR}/..
%cmake_build

%check
echo "void f(int *a, const cudaDeviceProp *b) { cudaChooseDevice(a,b); }" > b.cu
echo "void f(int *a, const hipDeviceProp_t *b) { hipChooseDevice(a,b); }" > e.hip
./bin/hipify-perl b.cu -o t.hip
diff e.hip t.hip

%install
%cmake_install
rm -rf %{buildroot}/usr/hip
# Fix executable perm:
chmod a+x %{buildroot}%{_bindir}/*
# Fix script shebang (Fedora doesn't allow using "env"):
sed -i 's|\(/usr/bin/\)env perl|\1perl|' %{buildroot}%{_bindir}//hipify-perl

%files
%doc README.md
%license LICENSE.txt
%{_bindir}/hipconvertinplace-perl.sh
%{_bindir}/hipconvertinplace.sh
%{_bindir}/hipexamine-perl.sh
%{_bindir}/hipexamine.sh
%{_bindir}/hipify-clang
%{_bindir}/hipify-perl
%{_libexecdir}/%{name}

%changelog
%autochangelog
