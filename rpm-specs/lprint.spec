# the package can work with devices from network, so use hardened build
%global _hardened_build 1

Name: lprint
Version: 1.3.1
Release: 6%{?dist}
Summary: A Label Printer Application

License: Apache-2.0
URL: https://www.msweet.org/lprint
Source0: https://github.com/michaelrsweet/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1: lprint.conf


# UPSTREAM PATCHES
# fix putting state file into correct place
# https://github.com/michaelrsweet/lprint/commit/648bc20171
Patch001: 0001-Update-state-filename-to-current-PAPPL-standard-rena.patch
# https://github.com/michaelrsweet/lprint/pull/151
Patch002: 0001-lprint.c-Enable-TLS-support-in-Web-UI.patch

# uses CUPS API for arrays, options, rastering, HTTP, IPP support
BuildRequires: pkgconfig(cups) >= 2.4.0
# written in C
BuildRequires: gcc
# for autosetup
BuildRequires: git-core
# uses Makefile
BuildRequires: make
# the basic printer application related structures are now implemented in PAPPL
BuildRequires: pkgconfig(pappl) >= 1.2
# using pkg-config in configure script
BuildRequires: pkgconf-pkg-config
# for macros in rpm scriptlets
BuildRequires: systemd-rpm-macros

# lprint server can run as a systemd service, but to don't require systemd by default,
# require filesystem (provides /usr/lib/systemd/system too)
Requires: filesystem
# uses password-auth PAM module from authselect
Requires: authselect-libs

%description
LPrint is a label printer application for macOS and Linux. Basically,
LPrint is a print spooler optimized for label printing. It accepts
"raw" print data as well as PNG images (like those used for shipping
labels by most shippers' current web APIs) and has built-in "drivers"
to send the print data to USB and network-connected label printers.


%prep
%autosetup -S git


%build
# use gcc
export CC=%{__cc}

# get system default CFLAGS and LDFLAGS
%set_build_flags

%configure 
%make_build


%install
%make_install DESTDIR=''

install -p -D -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/lprint.conf

%pre
if [ $1 -gt 1 ]
then
    if test ! -f /var/lib/lprint.state -a -f /etc/lprint.conf
    then
        # if the lprint.conf is the default one from RPM, do not move
        grep -q "^# Default configuration" /etc/lprint.conf || mv -f /etc/lprint.conf /var/lib/lprint.state
    fi
fi

%post
%systemd_post lprint.service

%preun
%systemd_preun lprint.service

%postun
%systemd_postun_with_restart lprint.service

%files
%doc README.md DOCUMENTATION.md CONTRIBUTING.md CHANGES.md
%license LICENSE NOTICE
%config(noreplace) %{_sysconfdir}/lprint.conf
%{_bindir}/lprint
%{_mandir}/man1/lprint-add.1*
%{_mandir}/man1/lprint-cancel.1*
%{_mandir}/man1/lprint-default.1*
%{_mandir}/man1/lprint-delete.1*
%{_mandir}/man1/lprint-devices.1*
%{_mandir}/man1/lprint-drivers.1*
%{_mandir}/man1/lprint-jobs.1*
%{_mandir}/man1/lprint-modify.1*
%{_mandir}/man1/lprint-options.1*
%{_mandir}/man1/lprint-printers.1*
%{_mandir}/man1/lprint-server.1*
%{_mandir}/man1/lprint-shutdown.1*
%{_mandir}/man1/lprint-status.1*
%{_mandir}/man1/lprint-submit.1*
%{_mandir}/man1/lprint.1*
%{_mandir}/man5/lprint.conf.5*
%{_unitdir}/lprint.service


%changelog
* Wed Oct 16 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1.3.1-6
- fix the scriptlet - missing the full path

* Thu Aug 08 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1.3.1-5
- rebuild with new pappl

* Tue Aug 06 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1.3.1-4
- fix showing certificate pages in web ui

* Mon Jul 29 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1.3.1-3
- set common server settings by /etc/lprint.conf

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1.3.1-1
- 2262303 - lprint-1.3.1 is available

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1.2.0-4
- SPDX migration and require filesystem instead of systemd

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1.2.0-1
- 2157610 - lprint-1.2.0 is available

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 06 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.0-3
- path to lprint was hardcoded in service file

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Zdenek Dohnal <zdohnal@redhat.com> - 1.1.0-1
- 2035381 - lprint-1.1.0 is available

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.0-2
- use smaller git-core instead of git

* Mon Aug 17 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.0-1
- Initial import (#1867587)
