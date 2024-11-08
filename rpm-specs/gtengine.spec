%bcond_with debug

Name: gtengine
Summary: Library for computations in mathematics, graphics, image analysis, and physics
Version: 7.1
Release: %autorelease
Epoch: 1
# Automatically converted from old format: Boost - review is highly recommended.
License: BSL-1.0
URL: http://www.geometrictools.com
Source0: https://github.com/davideberly/GeometricTools/archive/GTE-version-%{version}/GeometricTools-GTE-version-%{version}.tar.gz

BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(egl)
BuildRequires: glibc-devel
BuildRequires: gcc-c++
BuildRequires: gcc
BuildRequires: cmake
BuildRequires: dos2unix
BuildRequires: libstdc++-devel
BuildRequires: make

%description
A library of source code for computing in the fields of mathematics,
graphics, image analysis, and physics.
The engine is written in C++ 11 and, as such, has portable access
to standard constructs for multithreading programming on cores.
The engine also supports high-performance computing using general
purpose GPU programming (GPGPU).
SIMD code is also available using Intel Streaming SIMD Extensions (SSE).

GTEngine requires OpenGL 4.5.0 (or later).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = 1:%{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package samples
Summary: Samples files of %{name}
Requires: %{name}%{?_isa} = 1:%{version}-%{release}
%description samples
This package contains samples files for
testing that use %{name}.

%prep
%autosetup -n GeometricTools-GTE-version-%{version}

# Remove -Werror flags (rhbz#1923590)
find . -type f \( -name "CMakeLists.txt" \) -exec sed -i 's| -Werror||g' '{}' \;

sed -i 's|GTE_VERSION_MINOR 5|GTE_VERSION_MINOR 6|g' -i GTE/CMakeLists.txt

%build
%define __cmake_in_source_build .
pushd GTE
%if %{with debug}
%cmake -DCMAKE_BUILD_TYPE:STRING=Debug -DBUILD_RELEASE_LIB:BOOL=ON -DBUILD_SHARED_LIB:BOOL=ON %_vpath_srcdir
%else
%cmake -DCMAKE_BUILD_TYPE:STRING=Release -DBUILD_RELEASE_LIB:BOOL=ON -DBUILD_SHARED_LIB:BOOL=ON %_vpath_srcdir
%endif
%make_build
popd

pushd GTE/Samples
%if %{with debug}
%cmake -DCMAKE_SKIP_RPATH:BOOL=ON -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DBUILD_RELEASE_LIB:BOOL=ON -DBUILD_SHARED_LIB:BOOL=ON %_vpath_srcdir
%else
%cmake -DCMAKE_SKIP_RPATH:BOOL=ON -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release \
 -DBUILD_RELEASE_LIB:BOOL=ON -DBUILD_SHARED_LIB:BOOL=ON %_vpath_srcdir
%endif
%make_build
popd

%install
echo 'Manual installation...'

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -pm 755 GTE/lib/ReleaseShared/* $RPM_BUILD_ROOT%{_libdir}/

ln -sf libgtapplications.so.7.0 $RPM_BUILD_ROOT%{_libdir}/libgtapplications.so
ln -sf libgtgraphics.so.7.0 $RPM_BUILD_ROOT%{_libdir}/libgtgraphics.so
ln -sf libgtmathematicsgpu.so.7.0 $RPM_BUILD_ROOT%{_libdir}/libgtmathematicsgpu.so
ln -sf libgtapplications.so.7.0 $RPM_BUILD_ROOT%{_libdir}/libgtapplications.so.7
ln -sf libgtgraphics.so.7.0 $RPM_BUILD_ROOT%{_libdir}/libgtgraphics.so.7
ln -sf libgtmathematicsgpu.so.7.0 $RPM_BUILD_ROOT%{_libdir}/libgtmathematicsgpu.so.7

mkdir -p $RPM_BUILD_ROOT%{_includedir}/GTE
cp -a GTE/Applications $RPM_BUILD_ROOT%{_includedir}/GTE/
cp -a GTE/Graphics $RPM_BUILD_ROOT%{_includedir}/GTE/
cp -a GTE/Mathematics $RPM_BUILD_ROOT%{_includedir}/GTE/
find $RPM_BUILD_ROOT%{_includedir}/GTE -type f -name "*.cpp" -exec rm -f '{}' \;

mkdir -p $RPM_BUILD_ROOT%{_includedir}/GTL
cp -a GTL/Mathematics $RPM_BUILD_ROOT%{_includedir}/GTL/
cp -a GTL/Utility $RPM_BUILD_ROOT%{_includedir}/GTL/
find $RPM_BUILD_ROOT%{_includedir}/GTL -type f -name "*.vcxproj" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_includedir}/GTL -type f -name "*.sln" -exec rm -f '{}' \;

## Install GTL files
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}
cp -a GTE/Samples $RPM_BUILD_ROOT%{_libexecdir}/%{name}/

# Remove unused files
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.h" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.cpp" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.filters" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.vcxproj" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.csproj" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.sln" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.gte" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.o" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "cmake*" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "CMake*" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "Makefile" -exec rm -f '{}' \;
find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type f -name "*.json" -exec rm -f '{}' \;

for i in `find $RPM_BUILD_ROOT%{_libexecdir}/%{name}/Samples -type d -name "CMakeFiles"`; do
 rm -rf $i
done
##

# Edit a pkg-config file
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gtengine.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

xthreadlib=-lpthread

Name: GTEngine
Description: Library for computations in mathematics, graphics, image analysis, and physics
Version: 7.0
Cflags: -I%{_includedir}/GTE
Libs: -lgtgraphics -lgtmathematicsgpu -lgtapplications
Libs.private: -lpthread
EOF

%files
%license LICENSE
%doc README.md
%{_libdir}/libgt*.so.7.0
%{_libdir}/libgt*.so.7

%files devel
%{_includedir}/GTE/
%{_includedir}/GTL/
%{_libdir}/libgt*.so
%{_libdir}/pkgconfig/gtengine.pc

%files samples
%doc GTE/*InstallationRelease.pdf GTL/Documentation/GTLUtility.pdf
%{_libexecdir}/%{name}/

%changelog
%autochangelog
