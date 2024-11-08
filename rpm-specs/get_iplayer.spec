Name:           get_iplayer
Version:        3.35
Release:        4%{?dist}
Summary:        Lists, records and streams BBC iPlayer TV and radio programmes

License:        GPL-3.0-or-later
URL:            https://github.com/get-iplayer/%{name}
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source:         get_iplayer.xml
Source:         get_iplayer.desktop

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  sed

BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Encode::Locale)
BuildRequires:  perl(Env)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::Seekable)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(LWP::ConnCache)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(open)
BuildRequires:  perl(PerlIO::encoding)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(Unicode::Normalize)
BuildRequires:  perl(URI)

Requires:       /usr/bin/ffmpeg
Requires:       AtomicParsley
Requires:       perl-interpreter
Requires:       perl(Encode::Locale)
Requires:       perl(Mojolicious) >= 4.63

%description
get_iplayer is a tool for listing, recording and streaming BBC iPlayer
television and radio programmes, and other programmes via 3rd-party
plugins.

%prep
%autosetup

%build
# Generate the manpage
./get_iplayer --manpage=get_iplayer.1 || :

%install
install -Dpm0755 -t %{buildroot}%{_bindir} get_iplayer
install -Dpm0644 -t %{buildroot}%{_mandir}/man1 get_iplayer.1
touch options
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/get_iplayer options
install -Dpm0644 -t %{buildroot}%{_datadir}/mime/packages %{SOURCE1}
desktop-file-install --dir=%{buildroot}/%{_datadir}/applications %{SOURCE2}

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/get_iplayer
%{_mandir}/man1/get_iplayer.1*
%dir %{_sysconfdir}/get_iplayer
%config(noreplace) %{_sysconfdir}/get_iplayer/options
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/get_iplayer.xml

%changelog
* Thu Sep 12 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 3.35-4
- Fix changelog ordering

* Thu Sep 12 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 3.35-3
- Merge latest changes from rpmfusion

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Peter Oliver <rpm@mavit.org.uk> - 3.35-1
- Update to version 3.35.

* Fri Dec 22 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 3.34-2
- Convert license tag to SPDX
- Rework specfile to follow the Fedora packaging guidelines
- Tidy up Requires and BuildRequires

* Sun Nov 19 2023 Peter Oliver <rpm@mavit.org.uk> - 3.34-1
- Update to version 3.34.

* Fri Oct 13 2023 Peter Oliver <rpm@mavit.org.uk> - 3.33-1
- Update to version 3.33.

* Thu Oct 12 2023 Peter Oliver <rpm@mavit.org.uk> - 3.32-1
- Update to version 3.32.

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 19 2023 Peter Oliver <rpm@mavit.org.uk> - 3.31-2
- Allow ffmpeg binary to be provided by ffmpeg-free package.

* Sun Jan 22 2023 Peter Oliver <rpm@mavit.org.uk> - 3.31-1
- Update to version 3.31.

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Mon May 30 2022 Peter Oliver <rpm@mavit.org.uk> - 3.30-1
- Update to version 3.30.

* Wed Feb  9 2022 Peter Oliver <rpm@mavit.org.uk> - 3.29-1
- Update to version 3.29.

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Peter Oliver <rpm@mavit.org.uk> - 3.28-1
- Update to version 3.28.

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 15 2021 Peter Oliver <rpm@mavit.org.uk> - 3.27-1
- Update to version 3.27.

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 28 2020 Peter Oliver <rpm@mavit.org.uk> - 3.26-1
- Update to version 3.26.

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Feb  3 2020 Peter Oliver <rpm@mavit.org.uk> - 3.25-1
- Update to version 3.25.

* Fri Jan  3 2020 Peter Oliver <rpm@mavit.org.uk> - 3.24-1
- Update to version 3.24.

* Mon Dec  2 2019 Peter Oliver <rpm@mavit.org.uk> - 3.23-1
- Update to version 3.23.

* Tue Aug 20 2019 Peter Oliver <rpm@mavit.org.uk> - 3.22-1
- Update to version 3.22.

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Peter Oliver <rpm@mavit.org.uk> - 3.21-1
- Update to version 3.21.

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Feb 26 2019 Peter Oliver <rpm@mavit.org.uk> - 3.20-1
- Update to version 3.20.

* Sat Dec 29 2018 Peter Oliver <rpm@mavit.org.uk> - 3.18-1
- Update to version 3.18.

* Sun Aug 19 2018 Peter Oliver <rpm@mavit.org.uk> - 3.17-1
- Update to version 3.17.

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul  7 2018 Peter Oliver <rpm@mavit.org.uk> - 3.16-1
- Update to version 3.16.

* Wed Jun 20 2018 Peter Oliver <rpm@mavit.org.uk> - 3.14-1
- Update to version 3.14.

* Sat Mar 31 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.13-2
- Remove all scriplets for fedora
- Fix inconsistent use of the buildroot macro

* Tue Mar 27 2018 Peter Oliver <rpm@mavit.org.uk> - 3.13-1
- Update to version 3.13.

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Peter Oliver <rpm@mavit.org.uk> - 3.12-1
- Update to version 3.12.

* Sun Oct 29 2017 Peter Oliver <rpm@mavit.org.uk> - 3.06-1
- Update to version 3.06.

* Fri Oct 13 2017 Peter Oliver <rpm@mavit.org.uk> - 3.05-1
- Update to version 3.05.

* Mon Oct  2 2017 Peter Oliver <rpm@mavit.org.uk> - 3.03-1
- Update to version 3.03.

* Mon Aug 21 2017 Peter Oliver <rpm@mavit.org.uk> - 3.02-1
- Update to version 3.02.

* Fri Jul 14 2017 Paul Howarth <paul@city-fan.org> - 3.01-2
- Rebuild for Perl 5.26
- BR: and R: perl-interpreter
  (https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules)

* Mon May  8 2017 Peter Oliver <rpm@mavit.org.uk> - 3.01-1
- Update to version 3.01.

* Mon May  1 2017 Peter Oliver <rpm@mavit.org.uk> - 3.00-1
- Update to version 3.00.
- Drop unneeded dependencies.

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 13 2017 Peter Oliver <rpm@mavit.org.uk> - 2.99-1
- Update to version 2.99.

* Thu Feb  9 2017 Peter Oliver <rpm@mavit.org.uk> - 2.98-1
- Update to version 2.98.

* Mon Oct 24 2016 Paul Howarth <paul@city-fan.org> - 2.97-2
- BR: perl-generators
  (https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl)
- Add various other perl module dependencies
- Resolve rpmlint warning about mixed use of spaces and tabs
- Use %%license where available
- Drop %%defattr, redundant since rpm 4.4

* Thu Sep 29 2016 Peter Oliver <git@mavit.org.uk> - 2.97-1
- New upstream release 2.97

* Sun Aug 28 2016 Peter Oliver <rpm@mavit.org.uk> - 2.96-1
- New upstream release 2.96

* Sun Jul 24 2016 Peter Oliver <rpm@mavit.org.uk> - 2.95-3
- Add missing scriptlets.
- Fix typos.

* Sun Jul 24 2016 Peter Oliver <rpm@mavit.org.uk> - 2.95-2
- Handle `bbc-ipd:` URLs.
- Eliminate spurious module dependencies.

* Sun Jul 24 2016 Peter Oliver <rpm@mavit.org.uk> - 2.95-1
- Update to 2.95.
- Remove deprecated options from default system options file.
- Add dependency on XML::LibXML.

* Thu Jun  4 2015 David Woodhouse <dwmw2@infradead.org> - 2.94-1
- Update to 2.94.

* Sat Apr  4 2015 Peter Oliver <rpm@mavit.org.uk> - 2.92-2
- Set tag_longdesc option by default, since that's what Fedora's
  AtomicParsley supports.  Fixes bug 3541.

* Sat Apr  4 2015 Peter Oliver <rpm@mavit.org.uk> - 2.92-1
- Update to 2.92.

* Sat Dec 27 2014 Peter Oliver <rpm@mavit.org.uk> - 2.91-1
- Update to 2.91.

* Mon Nov  3 2014 David Woodhouse <dwmw2@infradead.org> - 2.90-1
- Update to 2.90.

* Sun Apr 20 2014 Peter Oliver <rpm@mavit.org.uk> - 2.86-1
- Update to 2.86.

* Sat Mar  8 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-8
- Bump version number.

* Fri Feb 28 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-7
- Functionality is improved if XML::Simple is installed, so add it as a
  dependency.  Bug #3137.

* Fri Feb 28 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-6
- Restore dependency filtering, required again now that
  https://bugzilla.redhat.com/show_bug.cgi?id=1051598 is fixed.  Fixes
  bug #3181.

* Sun Feb 16 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-5
- Depend on AtomicParsley (now packaged for Fedora 20).

* Thu Jan 16 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-4
- Remove workaround for RHBZ#1051607, fixed in file-libs-5.14-14.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-3
- Manually list Requires.  Works around
  https://bugzilla.redhat.com/show_bug.cgi?id=1051607 and fixes
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=3068.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-2
- README.txt replaced by README.md.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-1
- Update to 2.85.  Fixes bug #2862.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.80-8
- Depend on package vlc-core (which contains cvlc), not vlc.  Fixes bug #2143.

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.80-7
- Rebuilt for x264/FFmpeg

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.80-6
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-4
- conditionalise %%filter_setup properly.

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-3
- Make the requires filtering work in rpmfusion build system

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-2
- Remove superfluous perl requires

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-1
- Update to 2.80
- Add 'packagemanager yum' to options file (#1270)

* Sun Jan 09 2011 David Woodhouse <dwmw2@infradead.org> 2.79-1
- Update to 2.79

* Fri May 28 2010 David Woodhouse <dwmw2@infradead.org> 2.78-1
- Update to 2.78 (proper fix for Akamai).

* Wed May 26 2010 David Woodhouse <dwmw2@infradead.org> 2.77-3
- Add all necessary perl BuildRequires so we can generate man page

* Wed May 26 2010 David Woodhouse <dwmw2@infradead.org> 2.77-2
- BR perl(HTML::Entities) for man page

* Wed May 26 2010 David Woodhouse <dwmw2@infradead.org> 2.77-1
- Update to 2.77 (fix Limelight and Akamai RTMP downloads).

* Tue Apr 20 2010 David Woodhouse <dwmw2@infradead.org> 2.76-1
- Initial package
