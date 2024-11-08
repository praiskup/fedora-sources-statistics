Name:           mmtests
Version:        0.27
Release:        %autorelease
Summary:        Configurable test framework

License:        GPL-2.0-only
URL:            https://github.com/gormanm/mmtests
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source:         %{name}.rpmlintrc

BuildArch:      noarch
# /usr/bin/cpupower not available
ExcludeArch:    s390x

# for py3_shebang_fix
%if 0%{?rhel} && 0%{?rhel} <= 9
# for pathfix.py, used in older releases
BuildRequires:  python3-devel
%else
# pathfix.py removed in Python >= 3.12
# https://fedoraproject.org/wiki/Changes/Python3.12#pathfix.py_tool_will_be_removed
BuildRequires:  python3
%endif
BuildRequires:  python3-rpm-macros
# dependencies documented in run-mmtests.sh
Requires:       autoconf
Requires:       automake
Requires:       libtool
Requires:       make
Requires:       patch
Requires:       bc
Requires:       binutils-devel
Requires:       bzip2
Requires:       coreutils
Requires:       /usr/bin/cpupower
Requires:       e2fsprogs
Requires:       expect-devel
Requires:       gawk
Requires:       gcc
Requires:       gzip
Requires:       hdparm
Requires:       hostname
Requires:       hwloc
Requires:       iproute
Requires:       netcat
Requires:       numactl
Requires:       perl(File::Slurp)
Requires:       perl(Time::HiRes)
Requires:       psmisc
Requires:       tcl
Requires:       time
Requires:       util-linux
Requires:       wget
Requires:       which
Requires:       xfsprogs
Requires:       xfsprogs-devel
Requires:       xz
# not in EL9
Recommends:     btrfs-progs
# dependencies documented in README.md
Recommends:     perl(List::BinarySearch)
Recommends:     perl(Math::Gradient)

%description
MMTests is a configurable test suite that runs a number of common workloads
of interest to developers. It is possible to add monitors for the workload
and it provides reporting tools for comparing different test runs.


%prep
%autosetup -p1
%py3_shebang_fix bin/split-monitor-logs


%build


%install
install -d %{buildroot}%{_libexecdir}/MMTests
cp -pr \
  bin bin-virt configs drivers monitors shellpack_src shellpacks \
  stap-scripts config host_config *.sh \
  %{buildroot}%{_libexecdir}/MMTests


%files
%license COPYING
%doc README.md docs
%{_libexecdir}/MMTests


%changelog
%autochangelog
- 
