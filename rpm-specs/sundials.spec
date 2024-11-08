## Debug builds?
%bcond_with debug
#

# Enable pthread support
%bcond_with pthread
#

%define _legacy_common_support 1
%define _lto_cflags %{nil}

%global with_mpich 1
%if 0%{?fedora} >= 40
%ifarch %{ix86}
%global with_openmpi 0
%else
%global with_openmpi 1
%endif
%else
%global with_openmpi 1
%endif

## BLAS ##
%if 0%{?fedora} || 0%{?rhel} >= 9
%global blaslib flexiblas
%global blasvar %{nil}
%else
%global blaslib openblas
%global blasvar o
%endif
###########

%global with_hypre 1
%ifarch x86_64
%global with_openmpicheck 1
%global with_mpichcheck 0
%endif
###########
%global with_sercheck 1

## PETSc ##
%global with_petsc 1
###########

## SuperLUMT ##
%global with_superlumt 1
###########

## superlu_dist ##
%global with_superludist 0
###########

%if 0%{?rhel} && 0%{?rhel} >= 9
# KLU support
%global with_klu   1
%global with_klu64 1
##########
# Fortran
%if 0%{?with_klu64}
%global with_fortran 1
%endif
%if 0%{?with_klu}
%global with_fortran 0
%endif
##########
%endif
%if 0%{?fedora}
%ifarch s390x x86_64 %{power64} aarch64
%global with_klu64 1
%global with_fortran 1
%endif
%ifarch %{arm} %{ix86}
%global with_klu 1
%global with_fortran 0
%endif
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
%global with_klu 1
%global with_fortran 0
%endif
##########
# SOVERSIONs (*_SOVERSION from CMakeLists.txt):
%global arkodelib_SOVERSION 5
%global cvodelib_SOVERSION 6
%global cvodeslib_SOVERSION 6
%global idalib_SOVERSION 6
%global idaslib_SOVERSION 5
%global kinsollib_SOVERSION 6
#global cpodeslib_SOVERSION 0
%global nveclib_SOVERSION 6
%global sunmatrixlib_SOVERSION 4
%global sunlinsollib_SOVERSION 4
%global sunnonlinsollib_SOVERSION 3
%global sundialslib_SOVERSION 6

Summary:    Suite of nonlinear solvers
Name:       sundials
Version:    6.7.0
Release:    %autorelease
License:    BSD-3-Clause
URL:        https://computation.llnl.gov/projects/%{name}/
Source0:    https://github.com/LLNL/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

# This patch rename superLUMT library
Patch0:     %{name}-5.5.0-set_superlumt_name.patch

# This patch rename superLUMT64 library
Patch1:     %{name}-5.5.0-set_superlumt64_name.patch

Patch2:     %{name}-change_petsc_variable.patch
Patch3:     %{name}-klu64.patch

BuildRequires: make
%if 0%{?with_fortran}
BuildRequires: gcc-gfortran
%endif
BuildRequires: python3-devel
BuildRequires: gcc, gcc-c++
%if 0%{?epel}
BuildRequires: epel-rpm-macros
%endif
BuildRequires: cmake >= 3.10
BuildRequires: %{blaslib}-devel
%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64
BuildRequires: SuperLUMT64-devel
%endif
%ifarch %{arm} %{ix86}
BuildRequires: SuperLUMT-devel
%endif
%endif

# KLU support
%if 0%{?with_klu64}
BuildRequires: suitesparse64-devel
%endif
%if 0%{?with_klu}
BuildRequires: suitesparse-devel
%endif
##########

%if 0%{?with_fortran}
BuildRequires: gcc-gfortran%{?_isa}
%endif

%description
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.

SUNDIALS was implemented with the goal of providing robust time integrators
and nonlinear solvers that can easily be incorporated into existing simulation
codes. The primary design goals were to require minimal information from the
user, allow users to easily supply their own data structures underneath the
solvers, and allow for easy incorporation of user-supplied linear solvers and
preconditioners. 

%package devel
Summary:    Suite of nonlinear solvers (developer files)
Requires:   %{name}%{?_isa} = %{version}-%{release}
Provides:   %{name}-fortran-static = %{version}-%{release}
%description devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the developer files (.so file, header files).
#############################################################################
#########
%if 0%{?with_openmpi}
%package openmpi
Summary:    Suite of nonlinear solvers
BuildRequires: openmpi-devel
BuildRequires: hypre-openmpi-devel
%if 0%{?with_petsc}
BuildRequires: petsc-openmpi-devel >= 3.10
BuildRequires: scalapack-openmpi-devel
BuildRequires: hdf5-openmpi-devel
%endif
%if 0%{?with_superludist}
BuildRequires: superlu_dist-openmpi-devel
%endif

%if 0%{?with_fortran}
BuildRequires: gcc-gfortran%{?_isa}
%endif

%description openmpi
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel OpenMPI libraries.

%package openmpi-devel
Summary:    Suite of nonlinear solvers
Requires:   %{name}-openmpi%{?_isa} = %{version}-%{release}
Provides:   %{name}-openmpi-fortran-static = %{version}-%{release}
%description openmpi-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel OpenMPI devel libraries and
header files.

%if 0%{?with_fortran}
Requires: gcc-gfortran%{?_isa}
%endif

%endif
######
###############################################################################
######
%if 0%{?with_mpich}
%package mpich
Summary:    Suite of nonlinear solvers
BuildRequires: mpich-devel
BuildRequires: hypre-mpich-devel
%if 0%{?with_petsc}
BuildRequires: petsc-mpich-devel >= 3.10
BuildRequires: scalapack-mpich-devel
BuildRequires: hdf5-mpich-devel
%endif
%if 0%{?with_superludist}
BuildRequires: superlu_dist-mpich-devel
%endif

%if 0%{?with_fortran}
BuildRequires: gcc-gfortran%{?_isa}
%endif

%description mpich
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH libraries.

%package mpich-devel
Summary:    Suite of nonlinear solvers
Requires:   %{name}-mpich%{?_isa} = %{version}-%{release}
Provides:   %{name}-mpich-fortran-static = %{version}-%{release}
%description mpich-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH devel libraries and
header files.

%if 0%{?with_fortran}
Requires: gcc-gfortran%{?_isa}
%endif

%endif
######
#############################################################################

%package doc
Summary:    Suite of nonlinear solvers (documentation)
BuildArch: noarch
Obsoletes: sundials-doc < 0:6.6.2-5
%description doc
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the documentation files.

%prep
%setup -qc

pushd %{name}-%{version}

%ifarch s390x x86_64 %{power64} aarch64
%patch 1 -p0 -b .set_superlumt64_name
%endif
%ifarch %{arm} %{ix86}
%patch 0 -p0 -b .set_superlumt_name
%endif

%if 0%{?with_klu64}
%patch 3 -p1 -b .klu64
%endif

mv src/arkode/README.md src/README-arkode.md
mv src/cvode/README.md src/README-cvode.md
mv src/cvodes/README.md src/README-cvodes.md
mv src/ida/README.md src/README-ida.md
mv src/idas/README.md src/README.idas.md
mv src/kinsol/README.md src/README-kinsol.md
popd

%if 0%{?with_openmpi}
cp -a sundials-%{version} buildopenmpi_dir
%endif
%if 0%{?with_mpich}
cp -a sundials-%{version} buildmpich_dir
%endif

%build

%global _smp_ncpus_max 1

mkdir -p sundials-%{version}/build

export LIBBLASLINK=-l%{blaslib}%{blasvar}
export INCBLAS=%{_includedir}/%{blaslib}

%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%endif


%if %{with debug}
%undefine _hardened_build
export CFLAGS=" "
export FFLAGS=" "
export FCFLAGS=" "
%{_bindir}/cmake -B sundials-%{version}/build -S sundials-%{version} \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_CXX_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK" \
%else
export CFLAGS="%{build_cflags}"
export FFLAGS="%{build_fflags}"
%cmake -B sundials-%{version}/build -S sundials-%{version} \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
%endif
%if 0%{?with_klu64}
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu64.so \
 -DAMD_LIBRARY=%{_libdir}/libamd64.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf64.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd64.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%endif
%if 0%{?with_klu}
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu.so \
 -DAMD_LIBRARY=%{_libdir}/libamd.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%endif
 -DSUNDIALS_BUILD_WITH_PROFILING:BOOL=OFF \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK" \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
 -DLAPACK_ENABLE:BOOL=OFF \
 -DCMAKE_MODULE_LINKER_FLAGS:STRING="%{__global_ldflags}" \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python3} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=ON \
 -DMPI_ENABLE:BOOL=OFF \
%if 0%{?with_fortran}
 -DF77_INTERFACE_ENABLE:BOOL=ON \
 -DEXAMPLES_ENABLE_F77:BOOL=ON \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DF2003_INTERFACE_ENABLE:BOOL=ON \
%endif
 -DEXAMPLES_ENABLE_F90:BOOL=ON \
 -DFortran_INSTALL_MODDIR:PATH=%{_fmoddir}/%{name} \
%endif
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
%if %{with pthread}
 -DPTHREAD_ENABLE:BOOL=ON \
%endif
 -DSUNDIALS_PRECISION:STRING=double \
%if 0%{?with_superlumt}
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
 -DSUPERLUDIST_ENABLE:BOOL=OFF \
 -DHYPRE_ENABLE:BOOL=OFF \
 -DEXAMPLES_INSTALL:BOOL=OFF \
 -DSUNDIALS_BUILD_WITH_MONITORING:BOOL=ON -Wno-dev

%make_build V=1 -C sundials-%{version}/build

#############################################################################
#######
%if 0%{?with_openmpi}

mkdir -p buildopenmpi_dir/build
%{_openmpi_load}

## Blas
export LIBBLASLINK=-l%{blaslib}%{blasvar}
export INCBLAS=%{_includedir}/%{blaslib}
##

## SuperLUMT
%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%endif

## Hypre
%if 0%{?with_hypre}
export LIBHYPRELINK="-L$MPI_LIB -lHYPRE"
%endif
##

# Force MPI compilers
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
%if 0%{?fedora}
export FC=$MPI_BIN/mpifort
%else
export FC=$MPI_BIN/mpif77
%endif
##

%if %{with debug}
%undefine _hardened_build
export CFLAGS=" "
export FFLAGS=" "
export FCFLAGS=" "
%{_bindir}/cmake  -B buildopenmpi_dir/build -S buildopenmpi_dir \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_CXX_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%else
export CFLAGS="%{build_cflags}"
export FFLAGS="%{build_fflags}"
%cmake -B buildopenmpi_dir/build -S buildopenmpi_dir \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
%endif
%if 0%{?with_klu64}
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu64.so \
 -DAMD_LIBRARY=%{_libdir}/libamd64.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf64.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd64.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
 -DPETSC_ENABLE:BOOL=OFF \
%endif
%if 0%{?with_klu}
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu.so \
 -DAMD_LIBRARY=%{_libdir}/libamd.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%if 0%{?with_petsc}
 -DPETSC_ENABLE:BOOL=ON \
 -DPETSC_INCLUDES:PATH=$MPI_INCLUDE/petsc \
 -DPETSC_LIBRARIES:PATH=$MPI_LIB/libpetsc.so \
 -DPETSC_EXECUTABLE_RUNS:BOOL=ON \
%endif
%endif
 -DSUNDIALS_BUILD_WITH_PROFILING:BOOL=OFF \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
 -DMPI_INCLUDE_PATH:PATH=$MPI_INCLUDE \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE \
 -DLAPACK_ENABLE:BOOL=OFF \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}/openmpi/lib \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python3} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=ON \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
%if 0%{?with_fortran}
%if 0%{?fedora}
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpifort \
%else
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpif77 \
%endif
 -DF77_INTERFACE_ENABLE:BOOL=ON \
 -DEXAMPLES_ENABLE_F77:BOOL=ON \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DF2003_INTERFACE_ENABLE:BOOL=ON \
%endif
 -DEXAMPLES_ENABLE_F90:BOOL=ON \
 -DFortran_INSTALL_MODDIR:PATH=$MPI_FORTRAN_MOD_DIR/%{name} \
%endif
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
%if %{with pthread}
 -DPTHREAD_ENABLE:BOOL=ON \
%endif
%if 0%{?with_superlumt}
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
%if 0%{?with_superludist}
 -DSUPERLUDIST_ENABLE:BOOL=ON \
 -DSUPERLUDIST_INCLUDE_DIR:PATH=$MPI_INCLUDE/superlu_dist \
 -DSUPERLUDIST_LIBRARY_DIR:PATH=$MPI_LIB \
 -DSUPERLUDIST_LIBRARIES:STRING=libsuperlu_dist.so \
%endif
%if 0%{?with_hypre}
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=$MPI_INCLUDE/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DEXAMPLES_INSTALL:BOOL=OFF \
 -DSUNDIALS_BUILD_WITH_MONITORING:BOOL=ON -Wno-dev

%make_build V=1 -C buildopenmpi_dir/build
%{_openmpi_unload}
%endif
######
###########################################################################

%if 0%{?with_mpich}

mkdir -p buildmpich_dir/build
%{_mpich_load}

## Blas
export LIBBLASLINK=-l%{blaslib}%{blasvar}
export INCBLAS=%{_includedir}/%{blaslib}
##

## SuperLUMT
%if 0%{?with_superlumt}
%ifarch s390x x86_64 %{power64} aarch64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%endif

## Hypre
%if 0%{?with_hypre}
export LIBHYPRELINK="-L$MPI_LIB -lHYPRE"
%endif
##

# Force MPI compilers
export CC=$MPI_BIN/mpicc
export CXX=$MPI_BIN/mpic++
%if 0%{?fedora}
export FC=$MPI_BIN/mpifort
%else
export FC=$MPI_BIN/mpif77
%endif
##

%if %{with debug}
%undefine _hardened_build
export CFLAGS=" "
export FFLAGS=" "
export FCFLAGS=" "
%{_bindir}/cmake -B buildmpich_dir/build -S buildmpich_dir \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_CXX_FLAGS_DEBUG:STRING="-O0 -g %{__global_ldflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%else
export CFLAGS="%{build_cflags}"
export FFLAGS="%{build_fflags}"
%cmake -B buildmpich_dir/build -S buildmpich_dir \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
%endif
%if 0%{?with_klu64}
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu64.so \
 -DAMD_LIBRARY=%{_libdir}/libamd64.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf64.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd64.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
 -DPETSC_ENABLE:BOOL=OFF \
%endif
%if 0%{?with_klu}
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_LIBRARY=%{_libdir}/libklu.so \
 -DAMD_LIBRARY=%{_libdir}/libamd.so -DAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DBTF_LIBRARY=%{_libdir}/libbtf.so -DBTF_LIBRARY_DIR:PATH=%{_libdir} \
 -DCOLAMD_LIBRARY=%{_libdir}/libcolamd.so -DCOLAMD_LIBRARY_DIR:PATH=%{_libdir} \
 -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
%if 0%{?with_petsc}
 -DPETSC_ENABLE:BOOL=ON \
 -DPETSC_INCLUDES:PATH=$MPI_INCLUDE/petsc \
 -DPETSC_LIBRARIES:PATH=$MPI_LIB/libpetsc.so \
 -DPETSC_EXECUTABLE_RUNS:BOOL=ON \
%endif
%endif
 -DSUNDIALS_BUILD_WITH_PROFILING:BOOL=OFF \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
 -DLAPACK_ENABLE:BOOL=OFF \
 -DMPI_INCLUDE_PATH:PATH=$MPI_INCLUDE \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=$MPI_INCLUDE \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}/mpich/lib \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python3} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=ON \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
%if 0%{?with_fortran}
%if 0%{?fedora}
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpifort \
%else
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpif77 \
%endif
 -DF77_INTERFACE_ENABLE:BOOL=ON \
 -DEXAMPLES_ENABLE_F77:BOOL=ON \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DF2003_INTERFACE_ENABLE:BOOL=ON \
%endif
 -DEXAMPLES_ENABLE_F90:BOOL=ON \
 -DFortran_INSTALL_MODDIR:PATH=$MPI_FORTRAN_MOD_DIR/%{name} \
%endif
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
%if %{with pthread}
 -DPTHREAD_ENABLE:BOOL=ON \
%endif
%if 0%{?with_superlumt}
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
%if 0%{?with_superludist}
 -DSUPERLUDIST_ENABLE:BOOL=ON \
 -DSUPERLUDIST_INCLUDE_DIR:PATH=$MPI_INCLUDE/superlu_dist \
 -DSUPERLUDIST_LIBRARY_DIR:PATH=$MPI_LIB \
 -DSUPERLUDIST_LIBRARIES:STRING=libsuperlu_dist.so \
%endif
%if 0%{?with_hypre}
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=$MPI_INCLUDE/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DEXAMPLES_INSTALL:BOOL=OFF \
 -DSUNDIALS_BUILD_WITH_MONITORING:BOOL=ON -Wno-dev

%make_build V=1 -C buildmpich_dir/build
%{_mpich_unload}
%endif
######
#############################################################################

%install
%if 0%{?with_openmpi}
%{_openmpi_load}
%make_install -C buildopenmpi_dir/build
rm -f %{buildroot}$MPI_INCLUDE/sundials/LICENSE
rm -f %{buildroot}$MPI_INCLUDE/sundials/NOTICE
%{_openmpi_unload}
%endif

%if 0%{?with_mpich}
%{_mpich_load}
%make_install -C buildmpich_dir/build
rm -f %{buildroot}$MPI_INCLUDE/sundials/LICENSE
rm -f %{buildroot}$MPI_INCLUDE/sundials/NOTICE
%{_mpich_unload}
%endif

%make_install -C sundials-%{version}/build

# Remove files in bad position
rm -f %{buildroot}%{_prefix}/LICENSE
rm -f %{buildroot}%{_includedir}/sundials/LICENSE
rm -f %{buildroot}%{_includedir}/sundials/NOTICE

%check
%if 0%{?with_openmpi}
%if 0%{?with_openmpicheck}
%{_openmpi_load}
%define _vpath_builddir buildopenmpi_dir/build
%if %{with debug}
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
export OMPI_MCA_rmaps_base_oversubscribe=yes
%ctest -- -VV --output-on-failure --debug
%else
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
export OMPI_MCA_rmaps_base_oversubscribe=yes
%ctest -- --output-on-failure -E 'test_sunlinsol_superlumt|test_fsunlinsol_dense_mod'
%endif
%{_openmpi_unload}
%endif
## if with_openmpicheck
%endif
## if with_openmpi

%if 0%{?with_mpich}
%if 0%{?with_mpichcheck}
%{_mpich_load}
%define _vpath_builddir buildmpich_dir/build
%if %{with debug}
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
%ctest -- -VV --output-on-failure --debug
%else
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:$MPI_LIB
%ctest -- --output-on-failure -E 'test_sunlinsol_superlumt|test_fsunlinsol_dense_mod'
%endif
%{_mpich_unload}
%endif
## if with_mpichcheck
%endif
## if with_mpich

%if 0%{?with_sercheck}
%define _vpath_builddir sundials-%{version}/build
%if %{with debug}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_libdir}
%ctest -- -VV --output-on-failure --debug
%else
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_libdir}
%ctest -- --output-on-failure -E 'test_sunlinsol_superlumt|test_fsunlinsol_dense_mod'
%endif
%endif
## if with_sercheck

%files
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/src/README-arkode.md
%doc sundials-%{version}/src/README-cvode.md
%doc sundials-%{version}/src/README-cvodes.md
%doc sundials-%{version}/src/README-ida.md
%doc sundials-%{version}/src/README.idas.md
%doc sundials-%{version}/src/README-kinsol.md
%doc sundials-%{version}/NOTICE
%{_libdir}/libsundials_arkode*.so.%{arkodelib_SOVERSION}*
%{_libdir}/libsundials_cvode*.so.%{cvodelib_SOVERSION}*
%{_libdir}/libsundials_generic.so.%{sundialslib_SOVERSION}**
%{_libdir}/libsundials_ida.so.%{idalib_SOVERSION}*
%{_libdir}/libsundials_idas.so.%{idaslib_SOVERSION}*
%{_libdir}/libsundials_kinsol.so.%{kinsollib_SOVERSION}*
%{_libdir}/libsundials_nvecopenmp.so.%{nveclib_SOVERSION}*
%{_libdir}/libsundials_nvecmanyvector.so.%{nveclib_SOVERSION}*
%if %{with pthread}
%{_libdir}/libsundials_nvecpthreads.so.%{nveclib_SOVERSION}*
%endif
%{_libdir}/libsundials_nvecserial.so.%{nveclib_SOVERSION}*
%{_libdir}/libsundials_sunlinsol*.so.%{sunlinsollib_SOVERSION}*
%{_libdir}/libsundials_sunmatrix*.so.%{sunmatrixlib_SOVERSION}*
%{_libdir}/libsundials_sunnonlinsol*.so.%{sunnonlinsollib_SOVERSION}*
%if 0%{?with_fortran}
%{_libdir}/libsundials_f*[_mod].so.*
%endif

%files devel
%{_libdir}/*.a
%{_libdir}/libsundials_generic.so
%{_libdir}/libsundials_ida*.so
%{_libdir}/libsundials_cvode*.so
%{_libdir}/libsundials_arkode*.so
%{_libdir}/libsundials_kinsol.so
%{_libdir}/libsundials_nvecserial.so
%{_libdir}/libsundials_nvecopenmp.so
%{_libdir}/libsundials_nvecmanyvector.so
%{_libdir}/cmake/sundials/
%if %{with pthread}
%{_libdir}/libsundials_nvecpthreads.so
%endif
%{_libdir}/libsundials_sunmatrix*.so
%{_libdir}/libsundials_sunlinsol*.so
%{_libdir}/libsundials_sunnonlinsol*.so
%if 0%{?with_fortran}
%{_libdir}/libsundials_f*[_mod].so
%{_fmoddir}/%{name}/
%{_includedir}/sundials/sundials_futils.h
%if %{with pthread}
%{_libdir}/libsundials_fnvecpthreads.so
%endif
%if 0%{?with_superlumt}
%{_libdir}/libsundials_sunlinsolsuperlumt.so
%endif
%endif
%{_includedir}/nvector/
%{_includedir}/sunmatrix/
%{_includedir}/sunlinsol/
%{_includedir}/sunnonlinsol/
%{_includedir}/sunadaptcontroller/
%{_includedir}/sunmemory/
%{_includedir}/arkode/
%{_includedir}/cvode/
%{_includedir}/cvodes/
%{_includedir}/ida/
%{_includedir}/idas/
%{_includedir}/kinsol/
%dir %{_includedir}/sundials
%{_includedir}/sundials/sundials_export.h
%{_includedir}/sundials/sundials_band.h
%{_includedir}/sundials/sundials_dense.h
%{_includedir}/sundials/sundials_direct.h
%{_includedir}/sundials/sundials_iterative.h
%{_includedir}/sundials/sundials_linearsolver.h
%{_includedir}/sundials/sundials_math.h
%{_includedir}/sundials/sundials_matrix.h
%{_includedir}/sundials/sundials_memory.h
%{_includedir}/sundials/sundials_nonlinearsolver.h
%{_includedir}/sundials/sundials_mpi_types.h
%{_includedir}/sundials/sundials_nvector.h
%{_includedir}/sundials/sundials_types.h
%{_includedir}/sundials/sundials_version.h
%{_includedir}/sundials/sundials_config.h
%{_includedir}/sundials/sundials_base.hpp
%{_includedir}/sundials/sundials_context.h
%{_includedir}/sundials/sundials_context.hpp
%{_includedir}/sundials/sundials_convertibleto.hpp
%{_includedir}/sundials/sundials_linearsolver.hpp
%{_includedir}/sundials/sundials_logger.h
%{_includedir}/sundials/sundials_matrix.hpp
%{_includedir}/sundials/sundials_memory.hpp
%{_includedir}/sundials/sundials_nonlinearsolver.hpp
%{_includedir}/sundials/sundials_nvector.hpp
%{_includedir}/sundials/sundials_profiler.h
%{_includedir}/sundials/sundials_adaptcontroller.h
%{_includedir}/sundials/sundials_profiler.hpp

%if 0%{?with_openmpi}
%files openmpi
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/src/README-arkode.md
%doc sundials-%{version}/src/README-cvode.md
%doc sundials-%{version}/src/README-cvodes.md
%doc sundials-%{version}/src/README-ida.md
%doc sundials-%{version}/src/README.idas.md
%doc sundials-%{version}/src/README-kinsol.md
%doc sundials-%{version}/NOTICE
%{_libdir}/openmpi/lib/libsundials_generic.so.*
%{_libdir}/openmpi/lib/libsundials_nvecparallel.so.*
%{_libdir}/openmpi/lib/libsundials_nvecparhyp.so.*
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/openmpi/lib/libsundials_nvecpetsc.so.*
%{_libdir}/openmpi/lib/libsundials_sunnonlinsolpetscsnes.so.*
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/openmpi/lib/libsundials_nvecmpipthreads.so.*
%endif
%{_libdir}/openmpi/lib/libsundials_nvecmpiplusx.so.*
%{_libdir}/openmpi/lib/libsundials_kinsol.so.*
%{_libdir}/openmpi/lib/libsundials_ida*.so.*
%{_libdir}/openmpi/lib/libsundials_cvode*.so.*
%{_libdir}/openmpi/lib/libsundials_arkode*.so.*
%{_libdir}/openmpi/lib/libsundials_nvecserial.so.*
%{_libdir}/openmpi/lib/libsundials_nvecopenmp.so.*
%{_libdir}/openmpi/lib/libsundials_sunmatrix*.so.*
%{_libdir}/openmpi/lib/libsundials_sunlinsol*.so.*
%{_libdir}/openmpi/lib/libsundials_sunnonlinsol*.so.*
%{_libdir}/openmpi/lib/libsundials_nvecmanyvector.so.*
%{_libdir}/openmpi/lib/libsundials_nvecmpimanyvector.so.*
%if %{with pthread}
%{_libdir}/openmpi/lib/libsundials_nvecpthreads.so.*
%endif
%if 0%{?with_fortran}
%{_libdir}/openmpi/lib/libsundials_f*[_mod].so.*
%endif

%files openmpi-devel
%{_libdir}/openmpi/lib/*.a
%{_includedir}/openmpi-%{_arch}/nvector/
%{_includedir}/openmpi-%{_arch}/sundials/
%{_includedir}/openmpi-%{_arch}/arkode/
%{_includedir}/openmpi-%{_arch}/cvode/
%{_includedir}/openmpi-%{_arch}/cvodes/
%{_includedir}/openmpi-%{_arch}/ida/
%{_includedir}/openmpi-%{_arch}/idas/
%{_includedir}/openmpi-%{_arch}/kinsol/
%{_includedir}/openmpi-%{_arch}/sunlinsol/
%{_includedir}/openmpi-%{_arch}/sunmatrix/
%{_includedir}/openmpi-%{_arch}/sunnonlinsol/
%{_includedir}/openmpi-%{_arch}/sunmemory/
%{_includedir}/openmpi-%{_arch}/sunadaptcontroller/
%if 0%{?with_fortran}
%{_fmoddir}/openmpi/%{name}/
%{_libdir}/openmpi/lib/libsundials_f*[_mod].so
%endif
%{_libdir}/openmpi/lib/libsundials_generic.so
%{_libdir}/openmpi/lib/libsundials_nvecparallel.so
%{_libdir}/openmpi/lib/libsundials_nvecparhyp.so
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/openmpi/lib/libsundials_nvecpetsc.so
%{_libdir}/openmpi/lib/libsundials_sunnonlinsolpetscsnes.so
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/openmpi/lib/libsundials_nvecmpipthreads.so
%{_libdir}/openmpi/lib/libsundials_nvecpthreads.so
%endif
%{_libdir}/openmpi/lib/libsundials_nvecmpiplusx.so
%{_libdir}/openmpi/lib/libsundials_kinsol.so
%{_libdir}/openmpi/lib/libsundials_ida*.so
%{_libdir}/openmpi/lib/libsundials_cvode*.so
%{_libdir}/openmpi/lib/libsundials_arkode*.so
%{_libdir}/openmpi/lib/libsundials_nvecserial.so
%{_libdir}/openmpi/lib/libsundials_nvecopenmp.so
%{_libdir}/openmpi/lib/libsundials_sunmatrix*.so
%{_libdir}/openmpi/lib/libsundials_sunlinsol*.so
%{_libdir}/openmpi/lib/libsundials_sunnonlinsol*.so
%{_libdir}/openmpi/lib/libsundials_nvecmanyvector.so
%{_libdir}/openmpi/lib/libsundials_nvecmpimanyvector.so
%{_libdir}/openmpi/lib/cmake/sundials/
%endif

%if 0%{?with_mpich}
%files mpich
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/src/README-arkode.md
%doc sundials-%{version}/src/README-cvode.md
%doc sundials-%{version}/src/README-cvodes.md
%doc sundials-%{version}/src/README-ida.md
%doc sundials-%{version}/src/README.idas.md
%doc sundials-%{version}/src/README-kinsol.md
%doc sundials-%{version}/NOTICE
%{_libdir}/mpich/lib/libsundials_generic.so.*
%{_libdir}/mpich/lib/libsundials_nvecparallel.so.*
%{_libdir}/mpich/lib/libsundials_nvecparhyp.so.*
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/mpich/lib/libsundials_nvecpetsc.so.*
%{_libdir}/mpich/lib/libsundials_sunnonlinsolpetscsnes.so.*
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/mpich/lib/libsundials_nvecmpipthreads.so.*
%endif
%{_libdir}/mpich/lib/libsundials_nvecmpiplusx.so.*
%{_libdir}/mpich/lib/libsundials_kinsol.so.*
%{_libdir}/mpich/lib/libsundials_ida*.so.*
%{_libdir}/mpich/lib/libsundials_cvode*.so.*
%{_libdir}/mpich/lib/libsundials_arkode*.so.*
%{_libdir}/mpich/lib/libsundials_nvecserial.so.*
%{_libdir}/mpich/lib/libsundials_nvecopenmp.so.*
%{_libdir}/mpich/lib/libsundials_sunmatrix*.so.*
%{_libdir}/mpich/lib/libsundials_sunlinsol*.so.*
%{_libdir}/mpich/lib/libsundials_sunnonlinsol*.so.*
%{_libdir}/mpich/lib/libsundials_nvecmanyvector.so.*
%{_libdir}/mpich/lib/libsundials_nvecmpimanyvector.so.*
%if %{with pthread}
%{_libdir}/mpich/lib/libsundials_nvecpthreads.so.*
%endif
%if 0%{?with_fortran}
%{_libdir}/mpich/lib/libsundials_f*[_mod].so.*
%endif


%files mpich-devel
%{_includedir}/mpich-%{_arch}/nvector/
%{_includedir}/mpich-%{_arch}/sundials/
%{_includedir}/mpich-%{_arch}/arkode/
%{_includedir}/mpich-%{_arch}/cvode/
%{_includedir}/mpich-%{_arch}/cvodes/
%{_includedir}/mpich-%{_arch}/ida/
%{_includedir}/mpich-%{_arch}/idas/
%{_includedir}/mpich-%{_arch}/kinsol/
%{_includedir}/mpich-%{_arch}/sunlinsol/
%{_includedir}/mpich-%{_arch}/sunmatrix/
%{_includedir}/mpich-%{_arch}/sunnonlinsol/
%{_includedir}/mpich-%{_arch}/sunmemory/
%{_includedir}/mpich-%{_arch}/sunadaptcontroller/
%if 0%{?with_fortran}
%{_fmoddir}/mpich/%{name}/
%{_libdir}/mpich/lib/libsundials_f*[_mod].so
%endif
%{_libdir}/mpich/lib/*.a
%{_libdir}/mpich/lib/libsundials_generic.so
%{_libdir}/mpich/lib/libsundials_nvecparallel.so
%{_libdir}/mpich/lib/libsundials_nvecparhyp.so
%if 0%{?fedora}
%ifarch %{arm} %{ix86}
%if 0%{?with_petsc}
%{_libdir}/mpich/lib/libsundials_nvecpetsc.so
%{_libdir}/mpich/lib/libsundials_sunnonlinsolpetscsnes.so
%endif
%endif
%endif
%if %{with pthread}
%{_libdir}/mpich/lib/libsundials_nvecmpipthreads.so
%{_libdir}/mpich/lib/libsundials_nvecpthreads.so
%endif
%{_libdir}/mpich/lib/libsundials_nvecmpiplusx.so
%{_libdir}/mpich/lib/libsundials_kinsol.so
%{_libdir}/mpich/lib/libsundials_ida*.so
%{_libdir}/mpich/lib/libsundials_cvode*.so
%{_libdir}/mpich/lib/libsundials_arkode*.so
%{_libdir}/mpich/lib/libsundials_nvecserial.so
%{_libdir}/mpich/lib/libsundials_nvecopenmp.so
%{_libdir}/mpich/lib/libsundials_sunmatrix*.so
%{_libdir}/mpich/lib/libsundials_sunlinsol*.so
%{_libdir}/mpich/lib/libsundials_sunnonlinsol*.so
%{_libdir}/mpich/lib/libsundials_nvecmanyvector.so
%{_libdir}/mpich/lib/libsundials_nvecmpimanyvector.so
%{_libdir}/mpich/lib/cmake/sundials/
%endif

%files doc
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/NOTICE
%doc sundials-%{version}/doc/arkode/*.pdf
%doc sundials-%{version}/doc/ida*/*.pdf
%doc sundials-%{version}/doc/cvode*/*.pdf
%doc sundials-%{version}/doc/kinsol/*.pdf


%changelog
%autochangelog
