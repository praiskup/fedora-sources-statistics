%global upver 2016-01-26

# The license was changed after the most recent release in 2016.  We build from
# git so that the license information is current.
%global commit  e35b66d23729936bd475b31d933feca2b0021a13
%global date    20221005
%global forgeurl https://github.com/nwh/lusol

Name:           lusol
Version:        %(sed 's/-//g' <<< %{upver})
Summary:        LU factors of a square or rectangular sparse matrix

%forgemeta

Release:        %autorelease
License:        BSD-3-Clause OR MIT
URL:            https://web.stanford.edu/group/SOL/software/lusol/
VCS:            git:%{forgeurl}.git
Source:         %{forgesource}
# Fix calls to lu1rec that omit 1 parameter
# https://github.com/nwh/lusol/pull/11
Patch:          0001-Add-missing-parameter-to-lu1rec-calls.patch
# Fix use of an uninitialized value
# https://github.com/nwh/lusol/pull/12
Patch:          0002-Give-zero-a-value-before-use-in-lu8mod.patch
# Fix a race when building lusol.o
# https://github.com/nwh/lusol/pull/14
Patch:          0003-Fix-race-when-building-src-lusol.o.patch

# See https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  python3

%description
LUSOL computes LU factors of a square or rectangular sparse matrix.

%package        devel
Summary:        Header files and library links for LUSOL
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc-gfortran%{?_isa}

%description    devel
Header files and library links for developing applications that use
LUSOL.

%prep
%forgeautosetup -p1

# Force generated files to be regenerated
rm src/clusol.{c,h}

%build
# Use our build flags
sed -e 's|\(CFLAGS := \).*|\1%{build_cflags}|' \
    -e 's|\(F77FLAGS := \).*|\1%{build_fflags} -fdefault-integer-8|' \
    -e 's|\(F90FLAGS := \).*|\1%{build_fflags} -Jsrc|' \
    -e 's|\(LDFLAGS := \)-m64 -shared|\1%{build_ldflags} -shared -Wl,-h,libclusol.so.0|' \
    -e 's| -Wl,-rpath,/usr/lib||' \
    -i makefile

# Build the library
%make_build

%install
# The makefile has no install target
mkdir -p %{buildroot}%{_libdir}
cp -p src/libclusol.so %{buildroot}%{_libdir}/libclusol.so.0.0.0
ln -s libclusol.so.0.0.0 %{buildroot}%{_libdir}/libclusol.so.0
ln -s libclusol.so.0 %{buildroot}%{_libdir}/libclusol.so

mkdir -p %{buildroot}%{_includedir}
cp -p src/clusol.h %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_fmoddir}
cp -p src/lusol*.mod %{buildroot}%{_fmoddir}

%files
%doc CHANGES.md README.md src/lusol.txt
%license LICENSE.md
%{_libdir}/libclusol.so.0*

%files devel
%{_fmoddir}/lusol*.mod
%{_includedir}/clusol.h
%{_libdir}/libclusol.so

%changelog
%autochangelog
