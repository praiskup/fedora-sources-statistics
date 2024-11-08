%global opencsd_tag 7323ae88d16be4f9972b0ad60198963c64d70070

Name:           opencsd
Version:        1.5.4
Release:        0%{?dist}
Summary:        An open source CoreSight(tm) Trace Decode library

License:        BSD-3-Clause
URL:            https://github.com/Linaro/OpenCSD
Source0:        https://github.com/Linaro/OpenCSD/archive/%{opencsd_tag}.tar.gz

Patch0:         0001-hack-test.patch

BuildRequires:  patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make

%description
This library provides an API suitable for the decode of ARM(r)
CoreSight(tm) trace streams.

%package devel
Summary: Development files for the CoreSight(tm) Trace Decode library
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The opencsd-devel package contains headers and libraries needed
to develop CoreSight(tm) trace decoders.

%prep
%setup -q -n OpenCSD-%{opencsd_tag}
%patch -P0 -p1

%build
cd decoder/build/linux
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
LIB_PATH=%{_lib} make %{?_smp_mflags}


%install
cd decoder/build/linux
PREFIX=%{buildroot}%{_prefix} LIB_PATH=%{_lib} make install install_man DISABLE_STATIC=1 DEF_SO_PERM=755


%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} decoder/tests/run_pkt_decode_tests.bash -bindir %{buildroot}%{_bindir}/ use-installed

%files
%license LICENSE
%doc HOWTO.md README.md
%{_libdir}/*so\.*
%{_bindir}/*
%{_mandir}/man1/trc_pkt_lister.1.gz

%files devel
%doc decoder/docs/prog_guide/*
%{_includedir}/*
# no man files..
%{_libdir}/*so

#------------------------------------------------------------------------------
%changelog
* Thu Aug 29 2024 Jeremy Linton <jeremy.linton@arm.com> - 1.5.4-0
- Update to upstream 1.5.4

* Tue Aug 27 2024 Jeremy Linton <jeremy.linton@arm.com> - 1.5.3-1
- Ship the (newish) trc_pkt_lister man page, which is helpful and makes lint happy
- Also, enable some basic decoding unit tests that ship with opencsd after we tweak them.

* Tue Aug 27 2024 Jeremy Linton <jeremy.linton@arm.com> - 1.5.3-0
- Update to upstream 1.5.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar  5 2024 Jeremy Linton <jeremy.linton@arm.com> - 1.5.1-0
- Update to upstream 1.5.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Jeremy Linton <jeremy.linton@arm.com> - 1.4.1-0
- Update to upstream 1.4.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 15 2023 Jeremy Linton <jeremy.linton@arm.com> - 1.4.0-0
- Update to upstream 1.4.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Jeremy Linton <jeremy.linton@arm.com> - 1.3.3-0
- Update to upstream 1.3.3, and SPDX migration

* Fri Oct 14 2022 Jeremy Linton <jeremy.linton@arm.com> - 1.3.2-1
- Update to upstream 1.3.2

* Thu Aug  4 2022 Jeremy Linton <jeremy.linton@arm.com> - 1.3.1-1
- Update to upstream 1.3.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 24 2022 Jeremy Linton <jeremy.linton@arm.com> - 1.3.0-1
- Update to upstream 1.3.0

* Wed Jan 19 2022 Jeremy Linton <jeremy.linton@arm.com> - 1.2.0-1
- Update to upstream 1.2.0

* Fri Sep 10 2021 Jeremy Linton <jeremy.linton@arm.com> - 1.1.1-1
- Update to upstream 1.1.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 5 2021 Jeremy Linton <jeremy.linton@arm.com> - 1.0.0-1
- Update to upstream 1.0.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 23 2020 Jeremy Linton <jeremy.linton@arm.com> - 0.14.3-1
- Update to upstream 0.14.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Jeremy Linton <jeremy.linton@arm.com> - 0.14.1-1
- First opencsd package
