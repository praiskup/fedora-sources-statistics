Name:           aterm
Version:        1.0.1
Release:        43%{?dist}

Summary:        Afterstep XVT, VT102 emulator for the X Window system
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            http://aterm.sourceforge.net
Source0:        ftp://ftp.afterstep.org/apps/aterm/aterm-1.0.1.tar.bz2
Source1:        aterm.desktop
Patch0:         aterm-debuginfo.patch
Patch1:         aterm-stropts.patch
Patch2:         aterm-dpy.patch
Patch3:         aterm-configure-c99.patch

BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  libAfterImage-devel >= 1.07
BuildRequires:  libXt-devel
BuildRequires:  libXext-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  make
BuildRequires:  chrpath

# fix #454936
Requires: xorg-x11-fonts-misc

%description
aterm, version 1.00 is a colour vt102 terminal emulator, based on
rxvt 2.4.8 with Alfredo Kojima´s additions of fast transparency,
intended as an xterm(1) replacement for users who do not require fea-
tures such as Tektronix 4014 emulation and toolkit-style configurabil-
ity. As a result, aterm uses much less swap space -- a significant
advantage on a machine serving many X sessions.

%prep
%setup -q
%patch -P0 -b.debuginfo
%patch -P1 -b.stropts
%patch -P2 -p1 -b.dpy
%patch -P3 -p1 -b.configure-c99

%build
%configure --enable-fading --enable-background-image \
--enable-next-scroll --enable-utmp --enable-wtmp \
--enable-menubar --enable-graphics -enable-kanji \
--enable-big5 --enable-greek --enable-ttygid \
--enable-xgetdefault --with-term=rxvt \
--x-includes=%{_includedir} --x-libraries=%{_libdir}
%make_build


%install
%make_install INSTALL_PROGRAM="/usr/bin/install -c -m 755" 

desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}

chrpath --delete %{buildroot}%{_bindir}/aterm

%files
%doc ChangeLog ChangeLog.0.4
%doc doc/README.* doc/FAQ doc/ChangeLog.rxvt doc/menu/*
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/applications/%{name}.desktop


%changelog
* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0.1-43
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 27 2022 Florian Weimer <fweimer@redhat.com> - 1.0.1-37
- Port configure script to C99 (#2148747)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 06 2021 Jani Juhani Sinervo <jani@sinervo.fi> - 1.0.1-34
- Fix FTBFS for Rawhide and F35

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.0.1-17
- fix debuginfo. resolves rhbz#910549

* Sun Feb 10 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.0.1-16
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.0.1-15
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.0.1-14
- rebuild against new libjpeg

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.1-11
- Rebuild for new libpng

* Sat Feb 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.1-10
- fix dpy problem with new libAfterImage

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 14 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.1-8
- use gnome-xterm icon like xterm

* Sun Nov 14 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.1-7
- fixup desktop file (#617517)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.0.1-4
- fix #454936

* Sat Sep 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.0.1-3
- fix #440779

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.0.1-2
- Rebuilt for gcc43

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.1-1
- version upgrade
- new license tag

* Wed Feb 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-7
- fix #227377 (debuginfo package)

* Tue Sep 12 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-6
- FE6 rebuild

* Sun Jun 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-5
- fix #192433

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-4
- fix #177302 (term should really be rxvt with new termcap)

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-3
- Rebuild for Fedora Extras 5

* Tue Aug 16 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-1
- upgrade to stable
- add libAfterImage support
- add dist tag

* Thu Jun 23 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.00-0.1.beta4
- upgrade

* Fri Jun 03 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.00-0.1.beta3
- upgrade

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jun 22 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> 0:0.4.2-0.fdr.5
- changed Source0
- changed configure options ( both noticed by Adrian Reber )
* Sun Jun 22 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> 0:0.4.2-0.fdr.4
- removed Merged from aterm.desktop see bug #391 for details
* Sat Jun 21 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> 0:0.4.2-0.fdr.3
- added more documentation ( inspired by rxvt change noticed by Adrian Reber )
* Sat Jun 21 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> 0:0.4.2-0.fdr.2
- switched back to makeinstall
- added menu entry
- removed -n from setup
* Fri Jun 20 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de>
- Initial RPM release.
