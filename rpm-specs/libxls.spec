Name:           libxls
Version:        1.6.2
Release:        %autorelease -b 0
Summary:        Read binary Excel files from C/C++

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/libxls/libxls
Source0:        https://github.com/libxls/libxls/releases/download/v%{version}/%{name}-%{version}.tar.gz
# All for CVE-2021-27836
Patch0001:      https://github.com/libxls/libxls/pull/95.patch
Patch0002:      https://github.com/libxls/libxls/pull/96.patch
Patch0003:      https://github.com/libxls/libxls/pull/97.patch
# Fixes build with GCC 13
Patch0004:      https://github.com/libxls/libxls/pull/118.patch
# Fixes CVE-2023-38852
Patch0005:      https://github.com/libxls/libxls/pull/129.patch
Patch0006:      https://github.com/libxls/libxls/pull/131.patch

BuildRequires:  gcc-c++
BuildRequires:  make

%description
This is libxls, a C library for reading Excel files in the old binary OLE
format, plus a command-line tool for converting XLS to CSV (named,
appropriately enough, libxls2csv).


%package devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}


%prep
%autosetup -p1


%build
# Add prefix to not conflict executables with catdoc.
%configure --program-prefix=lib
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -delete


%check
PATH=%{buildroot}%{_bindir}:$PATH LD_LIBRARY_PATH=%{buildroot}%{_libdir} \
    make check || ( cat ./test-suite.log && exit 1 )


%files
%doc README.md AUTHORS
%license LICENSE
%{_bindir}/libxls2csv
%{_libdir}/libxlsreader.so.8
%{_libdir}/libxlsreader.so.8.*
%{_mandir}/man1/libxls2csv.1*

%files devel
%{_includedir}/xls.h
%{_includedir}/libxls
%{_libdir}/libxlsreader.so
%{_libdir}/pkgconfig/libxls.pc


%changelog
%autochangelog
