Name:           ptex
Version:        2.4.3
Release:        %autorelease
Summary:        Per-Face Texture Mapping for Production Rendering

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
Url:            https://github.com/wdas/%{name}
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz-devel
BuildRequires:  pkgconfig(zlib)

%description
Ptex is a texture mapping system developed by 
Walt Disney Animation Studios for production-quality rendering.

%package devel
Summary: Development files for the Ptex library
Requires:       %{name} = %{version}

%description devel
Development files for Walt Disney Animation Studios Ptex library.

%package doc
Summary: Documentation files for the Ptex library
BuildArch:      noarch

%description doc
Documentation files for Walt Disney Animation Studios Ptex library.

%package libs
Summary:        Libraries for Ptex

%description libs
This package contains the library needed to run programs dynamically
linked with Ptex.

%prep
%autosetup -n %{name}-%{version}


%build
%global _lto_cflags %{_lto_cflags} -ffat-lto-objects

# Detect package version
echo %{version} > version
%cmake \
        -DPTEX_BUILD_STATIC_LIBS=OFF 
%cmake_build


%install
%cmake_install

# Relocate .pc file
mv %{buildroot}%{_datadir}/pkgconfig %{buildroot}%{_libdir}

%files
%doc src/doc/README 
%license LICENSE        
%{_bindir}/ptxinfo

%files libs
%{_libdir}/libPtex.so.2.4

%files doc
%doc %{_datadir}/doc/Ptex

%files devel
%{_includedir}/Ptex*.h
%{_libdir}/cmake/Ptex
%{_libdir}/libPtex.so
%{_libdir}/pkgconfig/ptex.pc

%changelog
%autochangelog
