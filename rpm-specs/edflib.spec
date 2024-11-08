%global forgeurl https://gitlab.com/Teuniz/EDFlib
%global version0 1.27
%global tag0 v%{version0}
%forgemeta

Name:           edflib
Version:        %{forgeversion}
%global so_version 2
Release:        %autorelease
Summary:        C/C++ library to read/write EDF+ and BDF+ files

# The entire source is BSD-3-Clause, except:
#   - The executable sources sine_generator.c, sweep_generator.c,
#     test_edflib.c, and test_generator.c are all BSD-2-Clause, but the
#     binaries built from these sources are not installed; therefore these
#     sources do not contribute to the license of the binary RPMs.
#   - The contents of unittest/ are GPL-3.0-or-later, but the binaries that
#     link these sources are for testing only and are not installed; therefore
#     these sources do not contribute to the license of the binary RPMs.
License:        BSD-3-Clause
URL:            https://www.teuniz.net/edflib
# As of 1.26, we have switched to packaging from the automatic GitLab source
# archive instead; for 1.26, the release archive at:
#   %%global tar_version %%(echo '%%{version}' | tr -d .)
#   Source:         https://www.teuniz.net/edflib/edflib_%%{tar_version}.tar.gz
# lacked the lib/ subdirectory containing the Makefile, and had some other cruft
# in a tmp/ directory, indicating an error-prone manual release process.
Source:         %{forgesource}

# Library makefile: make more amenable to distribution packaging
# https://gitlab.com/Teuniz/EDFlib/-/merge_requests/7
# This PR seems to have languished upstream, and the project appears to have
# disabled merge requests at some point, so the link above is broken.
#
# - 1.27 broke ABI by changing EDFLIB_MAXSIGNALS, which affects the structure
#   edflib_hdr_t in the public API, this patch now sets an SONAME
Patch:          edflib-1.27-makefile.patch

# Big-endian support was proposed upstream, but a patch was declined, and
# beginning with version 1.23, “non-support” of big-endian architectures is
# explicitly documented and enforced at runtime. See the linked issue:
#
# edflib does not support big-endian architectures
# https://bugzilla.redhat.com/show_bug.cgi?id=2135034
#
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    s390x %{ix86}

BuildRequires:  make
BuildRequires:  gcc

%global common_description %{expand:
EDFlib is a programming library for C/C++ for reading and writing EDF+ and BDF+
files. It also reads “old style” EDF and BDF files. EDF means European Data
Format. BDF is the 24-bits version of EDF.

Documentation is available at https://www.teuniz.net/edflib/index.html.}

%description %common_description

Documentation is available at https://www.teuniz.net/edflib/index.html.


%package devel
Summary:        Development files for edflib
Requires:       edflib%{?_isa} = %{version}-%{release}

%description devel %common_description

The edflib-devel package contains libraries and header files for developing
applications that use edflib.


%prep
%autosetup %{forgesetupargs} -p1
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_flags
sed -r -i 's/-O[23]//' lib/makefile


%build
%make_build -C lib CC="${CC-gcc}" LDCONFIG='/bin/true' MYUID='0' \
    EXTRA_CFLAGS="${CFLAGS}" LDLIBS="${LDFLAGS-}"
%make_build -C unittest CC="${CC-gcc}" \
    CFLAGS="${CFLAGS-} -D_LARGEFILE64_SOURCE -D_LARGEFILE_SOURCE ${LDFLAGS-}"


%install
%make_install -C lib PREFIX='%{_prefix}' MYUID=0 LDCONFIG=/bin/true


%check
./unittest/edflib_test


%files
%license LICENSE
%doc README.md
%{_libdir}/libedf.so.%{so_version}


%files devel
%{_includedir}/edflib.h
%{_libdir}/libedf.so


%changelog
%autochangelog
