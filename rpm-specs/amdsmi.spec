%global rocm_release 6.2
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}
%global upstreamname amdsmi

# Downloads its own googletest
# Testing also depends on having AMD hardware cpu and/or gpu installed.
# Not suitable for a general %check
#
# Non root result for gfx1100 and this kernel 6.11.0-0.rc2.23.fc41.x86_64
# 25 pass, 5 fail
# No oops
%bcond_with test

Name:       amdsmi
Version:    %{rocm_version}
%if 0%{?rhel} < 10
Release:    1%{?dist}
%else
Release:    %autorelease
%endif
Summary:    AMD System Management Interface

License:    NCSA AND MIT AND BSD-3-Clause
URL:        https://github.com/RadeonOpenCompute/%{upstreamname}
Source0:    %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz
# esmi_ib_library is not suitable for packaging
# https://github.com/amd/esmi_ib_library/issues/13
# This tag was choosen by the amdsmi project because 4.0+ introduced variables not
# found in the upstream kernel.
%global esmi_ver 3.0.3
Source1:    https://github.com/amd/esmi_ib_library/archive/refs/tags/esmi_pkg_ver-%{esmi_ver}.tar.gz
# https://github.com/ROCm/amdsmi/pull/48
Patch0:     0001-Do-not-automatically-download-kernel-header-amd_hsmp.patch

ExclusiveArch: x86_64

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: kernel-devel
BuildRequires: libdrm-devel
BuildRequires: python3-devel

# University of Illinois/NCSA Open Source License
Provides: bundled(esmi_ib_library) = %{esmi_ver}

%description
The AMD System Management Interface Library, or AMD SMI library, is a C
library for Linux that provides a user space interface for applications
to monitor and control AMD devices.

%package devel
Summary: Libraries and headers for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

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
%autosetup -n %{upstreamname}-rocm-%{version} -p1
tar xf %{SOURCE1}
mv esmi_ib_library-* esmi_ib_library
# So we can pick up this license
mv esmi_ib_library/License.txt esmi_ib_library_License.txt 

# W: spurious-executable-perm /usr/share/doc/amdsmi/README.md
chmod a-x README.md

# /usr/libexec/amdsmi_cli/BDF.py:126: SyntaxWarning: invalid escape sequence '\.'
#   bdf_regex = "(?:[0-6]?[0-9a-fA-F]{1,4}:)?[0-2]?[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}\.[0-7]"
sed -i -e 's@bdf_regex = "@bdf_regex = r"@' amdsmi_cli/BDF.py

%build
%cmake \
    -DBUILD_KERNEL_ASM_DIR=/usr/include/asm \
%if %{with test}
    -DBUILD_TESTS=ON \
%endif

%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}/usr/share/amdsmi %{buildroot}/%{python3_sitelib}
mv %{buildroot}/usr/share/setup.cfg %{buildroot}/%{python3_sitelib}/amdsmi/
mv %{buildroot}/usr/share/pyproject.toml %{buildroot}/%{python3_sitelib}/amdsmi/

# Remove some things
rm -rf %{buildroot}/usr/share/example
rm %{buildroot}%{_docdir}/amd_smi-asan/LICENSE.txt
rm %{buildroot}%{_docdir}/amd_smi/LICENSE.txt
rm %{buildroot}%{_docdir}/amd_smi/README.md
rm %{buildroot}%{_datadir}/_version.py

# W: unstripped-binary-or-object /usr/lib/python3.13/site-packages/amdsmi/libamd_smi.so
# Does an explict open, so can not just rm it
# let's just strip it
strip %{buildroot}/%{python3_sitelib}/amdsmi/*.so
# E: non-executable-script .../amdsmi_cli/amdsmi_cli_exceptions.py 644 /usr/bin/env python3
chmod a+x %{buildroot}/%{_libexecdir}/amdsmi_cli/*.py

# RPM has a problem with this file
rm %{buildroot}%{_libdir}/cmake/amd_smi/amd_smi-config.cmake

%files
%doc README.md
%license License.txt
%license LICENSE
%license esmi_ib_library_License.txt 
%{_libdir}/libamd_smi.so.*
%{_bindir}/amd-smi
%{_libexecdir}/amdsmi_cli
%{python3_sitelib}/amdsmi

%files devel
%{_includedir}/amd_smi
%{_libdir}/libamd_smi.so
%{_libdir}/cmake/amd_smi

%if %{with test}
%files test
%{_datadir}/tests
%endif

%changelog
%autochangelog
