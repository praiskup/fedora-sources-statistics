%global abi 4

Name: libxmp
Version: 4.6.0
Release: 6%{?dist}
Summary: A multi-format module playback library
Source0: https://downloads.sourceforge.net/project/xmp/libxmp/%{version}/libxmp-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: make
Provides: bundled(md5-plumb)
# Automatically converted from old format: BSD and LGPLv2+ and MIT and Public Domain - review is highly recommended.
License: LicenseRef-Callaway-BSD AND LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-MIT AND LicenseRef-Callaway-Public-Domain
URL: http://xmp.sourceforge.net/

%description
Libxmp is a library that renders module files to PCM data. It supports
over 90 mainstream and obscure module formats including Protracker (MOD),
Scream Tracker 3 (S3M), Fast Tracker II (XM), and Impulse Tracker (IT).

Many compressed module formats are supported, including popular Unix, DOS,
and Amiga file packers including gzip, bzip2, SQSH, Powerpack, etc.

%package devel
Summary: A multi-format module playback library development files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake-filesystem

%description devel
Libxmp is a library that renders module files to PCM data. It supports
over 90 mainstream and obscure module formats including Protracker (MOD),
Scream Tracker 3 (S3M), Fast Tracker II (XM), and Impulse Tracker (IT).

Many compressed module formats are supported, including popular Unix, DOS,
and Amiga file packers including gzip, bzip2, SQSH, Powerpack, etc.

This package contains the header and development library.

%prep
%setup -q
for file in docs/Changelog ; do
        iconv -f iso8859-1 -t utf8 -o $file.utf $file && touch -r $file $file.utf && mv $file.utf $file
done

%build
%configure
%make_build

%install
%make_install
install -Dpm644 docs/libxmp.3 %{buildroot}%{_mandir}/man3/libxmp.3
chmod 755 %{buildroot}%{_libdir}/libxmp.so.*

%check
%make_build check

%files
%license docs/COPYING.LIB
%doc README docs/Changelog docs/CREDITS
%{_libdir}/libxmp.so.%{abi}{,.*}

%files devel
%doc docs/libxmp.html docs/libxmp.pdf docs/{fixloop,formats}.txt
%{_includedir}/xmp.h
%{_mandir}/man3/libxmp.3*
%{_libdir}/cmake/libxmp/libxmp-config-version.cmake
%{_libdir}/cmake/libxmp/libxmp-config.cmake
%{_libdir}/pkgconfig/libxmp.pc
%{_libdir}/libxmp.so

%changelog
* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 4.6.0-6
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Dominik Mierzejewski <dominik@greysector.net> - 4.6.0-1
- update to 4.6.0 (#2216871)
- drop obsolete patch
- fix SONAME glob in file list
- include cmake files

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Dominik Mierzejewski <rpm@greysector.net> - 4.5.0-1
- update to 4.5.0 (#1971814)
- ensure SONAME changes are noticed
- re-enable LTO
- use modern make_* macros

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 4.4.1-11
- Disable LTO

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Dominik Mierzejewski <rpm@greysector.net> 4.4.1-7
- add BR: gcc for https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot
- drop redundant ldconfig scriptlets and use make_install macro

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Dominik Mierzejewski <rpm@greysector.net> - 4.4.1-1
- update to 4.4.1 (#1384263)

* Fri Jul 29 2016 Dominik Mierzejewski <rpm@greysector.net> - 4.4.0-1
- update to 4.4.0 (#1358055)

* Wed Apr 27 2016 Dominik Mierzejewski <rpm@greysector.net> - 4.3.13-1
- update to 4.3.13 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.13/Changelog/view)
- mark COPYING.LIB with license macro

* Mon Mar 07 2016 Dominik Mierzejewski <rpm@greysector.net> - 4.3.12-1
- update to 4.3.12 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.12/Changelog/view)

* Mon Feb 15 2016 Dominik Mierzejewski <rpm@greysector.net> - 4.3.11-1
- update to 4.3.11 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.11/Changelog/view)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 02 2016 Dominik Mierzejewski <rpm@greysector.net> - 4.3.10-1
- update to 4.3.10 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.10/Changelog/view)
- use HTTPS for source URL

* Thu Jun 25 2015 Dominik Mierzejewski <rpm@greysector.net> - 4.3.9-1
- update to 4.3.9 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.9/Changelog/view)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Dominik Mierzejewski <rpm@greysector.net> - 4.3.8-1
- update to 4.3.8 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.8/Changelog/view)

* Mon Feb 09 2015 Dominik Mierzejewski <rpm@greysector.net> - 4.3.5-1
- update to 4.3.5 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.5/Changelog/view)

* Tue Jan 13 2015 Dominik Mierzejewski <rpm@greysector.net> - 4.3.4-1
- update to 4.3.4 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.4/Changelog/view)

* Mon Dec 08 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.3.2-1
- update to 4.3.2 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.2/Changelog/view)

* Wed Nov 12 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.3.1-1
- update to 4.3.1 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.1/Changelog/view)

* Thu Oct 09 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.3.0-1
- update to 4.3.0 (http://sourceforge.net/projects/xmp/files/libxmp/4.3.0/Changelog/view)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.8-1
- update to 4.2.8 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.8/Changelog/view)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.7-1
- update to 4.2.7 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.7/Changelog/view)

* Sun Mar 02 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.5-1
- update to 4.2.5 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.5/Changelog/view)

* Mon Feb 24 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.4-1
- update to 4.2.4 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.4/Changelog/view)
- drop the list of files with licenses other than LGPLv2.1+,
  it's growing too much

* Mon Jan 13 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.2-1
- update to 4.2.2

* Sun Nov 17 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.2.0-1
- update to 4.2.0 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.0/Changelog/view)
- add proper provides for bundled md5-plumb (version unknown)
- drop any mention of unzoo.c, it's gone from the source

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.1.5-1
- update to 4.1.5
- require the same arch of main package for -devel subpackage

* Wed May 29 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.1.4-1
- update to 4.1.4
- drop st02-ok sample from -devel doc (removed by upstream)
- review fixes

* Mon Apr 29 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.1.1-1
- initial build based on xmp.spec
