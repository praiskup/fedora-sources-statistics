# Blocked by perl-parallel-forker not being packaged
# https://bugzilla.redhat.com/show_bug.cgi?id=2268659
%bcond longtests 0

# Warnings in <F40 fails build
%if 0%{?fedora} <= 39
    %ifarch ppc64le
    %bcond ccwarn 0
    %endif
%else
    %bcond ccwarn 1
%endif

%bcond tcmalloc 1
%bcond ccache 0
%bcond mold 0

Name:           verilator
Version:        5.028
Release:        %autorelease
Summary:        A fast simulator for synthesizable Verilog
License:        LGPL-3.0-only OR Artistic-2.0
URL:            https://veripool.org/verilator/
Source0:        https://github.com/verilator/verilator/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

# Undesirable upstream, fixes warnings with FORTIFY_SOURCE
Patch:          0003-Enable-optimization-in-tests.patch

BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  coreutils
BuildRequires:  cmake
BuildRequires:  findutils
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  help2man
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl-lib
BuildRequires:  perl-version
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(strict)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(vars)
BuildRequires:  python3-devel
BuildRequires:  sed
%if %{with tcmalloc}
BuildRequires:  gperftools-libs
BuildRequires:  gperftools-devel
%endif
%if %{with mold}
Requires:       mold
%endif
%if %{with ccache}
BuildRequires:  ccache
%endif

# required for further tests
BuildRequires:  gdb

%description
Verilator is the fastest free Verilog HDL simulator. It compiles
synthesizable Verilog, plus some PSL, SystemVerilog and Synthesis
assertions into C++ or SystemC code. It is designed for large projects
where fast simulation performance is of primary concern, and is
especially well suited to create executable models of CPUs for
embedded software design teams.

%package devel
Summary:        Libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains library and header files needed to develop
applications based on %{name}.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains the documentation for %{name}.


%prep
%autosetup -p1
find . -name .gitignore -delete
export VERILATOR_ROOT=%{_datadir}
autoconf
%configure \
    --disable-partial-static \
    --enable-defenv \
%if %{with ccwarn}
    --enable-ccwarn \
%else 
    --disable-ccwarn \
%endif
%if %{with longtests}
    --enable-longtests
%else
    --disable-longtests
%endif

# We cannot run autoreconf because upstream uses unqualifed stdlib identifiers
# that are included by autoconf-generated header files.
find -name Makefile_obj -exec sed -i \
    -e 's|^\(COPT = .*\)|\1 %{optflags}|' \
    -e 's|^#LDFLAGS += .*|LDFLAGS += %{__global_ldflags}|' \
    {} \;

# Fix /usr/bin/env <bin> ("env-script-interpreter")
sed -i 's#/usr/bin/env python3#/usr/bin/python3#g' docs/bin/*

%build
export VERILATOR_SRC_VERSION=fedora-%{version}
%make_build 

%install
%make_install

# verilator installs verilator.pc under ${datadir}
# but for consistency we want it under ${libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_datadir}/pkgconfig/verilator.pc %{buildroot}%{_libdir}/pkgconfig

# some tests and examples are CC0 and cannot be packaged into Fedora
rm -rf %{buildroot}%{_datadir}/verilator/examples
rm -rf %{buildroot}%{_datadir}/verilator/tests

%check
make test 


%files
%license Artistic LICENSE
%{_mandir}/man1/*.1.gz
%{_bindir}/verilator
%{_bindir}/verilator_bin
%{_bindir}/verilator_bin_dbg
%{_bindir}/verilator_coverage
%{_bindir}/verilator_coverage_bin_dbg
%{_bindir}/verilator_gantt
%{_bindir}/verilator_profcfunc
%{_datadir}/verilator/bin

%files devel
%license Artistic LICENSE
%{_datadir}/verilator/include
%{_libdir}/pkgconfig/verilator.pc
%{_datadir}/verilator/verilator-config*.cmake

%files doc
%license Artistic LICENSE docs/guide/copyright.rst
%doc Changes README*
%doc docs

%changelog
%autochangelog
