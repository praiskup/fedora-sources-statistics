%global major_version 3
%global minor_version 0
%global full_version %{major_version}.%{minor_version}
%global soversion %{full_version}.0
%global srcversion esmi_pkg_ver-%{full_version}

# The documentation doesn't build at the moment, use the prebuilt one instead
%bcond_with doc

Name:           esmi_ib_library
Version:        %{full_version}
Release:        %autorelease
Summary:        E-SMI: EPYC System management Interface In-band Library

License:        NCSA
URL:            https://github.com/amd/esmi_ib_library
Source:         %{url}/archive/%{srcversion}/%{name}-%{srcversion}.tar.gz
Patch:          esmi-amd_hsmp-include.patch

# This is a hardware enablement package for AMD x86_64 platforms
ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  sed
%if %{with doc}
BuildRequires:  doxygen
BuildRequires:  make
BuildRequires:  texlive-latex
%endif

Suggests:       %{name}-doc = %{version}-%{release}

%description
The EPYC System Management Interface In-band Library, or E-SMI library, is
part of the EPYC System Management Inband software stack. It is a C library
for Linux that provides a user space interface to monitor and control the CPU's
power, energy, performance and other system management features.

%package        devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains development headers and libraries for %{name}.

%package        doc
Summary:        Additional documentation for %{name}
BuildArch:      noarch

%description    doc
This package contains additional documentation for %{name}.

%package -n     e_smi_tool
Summary:        E-SMI: EPYC™ System management Interface tool

%description -n e_smi_tool
This package contains E-SMI tool, a program based on the E-SMI In-band library
that provides options to Monitor and Control System Management functionality.

%prep
%setup -q -n %{name}-%{srcversion}

# The kernel on el8 and el9 is missing some includes we need so patch them in
%if 0%{?el8} || 0%{?el9}
%patch -P0 -p1
%endif

# Use FHS install paths and patch version detection
sed -i CMakeLists.txt \
    -e 's:${E_SMI}/bin:%{_bindir}:g' \
    -e 's:e_smi/include:%{_includedir}:g' \
    -e 's:${E_SMI}/lib/static:%{_libdir}:g' \
    -e 's:${E_SMI}/lib:%{_libdir}:g' \
    -e 's:${E_SMI}/doc:%{_pkgdocdir}:g' \
    -e 's:get_version_from_tag("1.0.0.0":get_version_from_tag("%{soversion}":'

%if %{with doc}
# Remove prebuilt docs
rm ESMI_IB_Release_Notes.pdf ESMI_Manual.pdf
%endif

%build
%cmake
%cmake_build
%if %{with doc}
make -C %{_vpath_builddir} doc
%endif

%install
%cmake_install

# Strip rpath
chrpath -d %{buildroot}/%{_bindir}/e_smi_tool

%check
%ctest

%files
%license License.txt
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%doc %{_pkgdocdir}/RELEASENOTES.md
%{_libdir}/libe_smi64.so.%{major_version}
%{_libdir}/libe_smi64.so.%{major_version}.%{minor_version}

%files devel
%{_includedir}/e_smi/
%{_libdir}/libe_smi64.so

%files doc
%license License.txt
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/ESMI_IB_Release_Notes.pdf
%doc %{_pkgdocdir}/ESMI_Manual.pdf

%files -n e_smi_tool
%{_bindir}/e_smi_tool

%changelog
%autochangelog
