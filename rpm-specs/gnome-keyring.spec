%global glib2_version 2.44.0
%global gcr_version 3.27.90
%global gcrypt_version 1.2.2

%bcond_without ssh_agent

Name:           gnome-keyring
Version:        46.2
Release:        %autorelease
Summary:        Framework for managing passwords and other secrets

# egg/ is (GPL-2.0-or-later OR LGPL-3.0-or-later) OR BSD-3-Clause
# pkcs11/ is MPL-1.1 OR GPL-2.0-or-later OR  LGPL-2.1-or-later
License:        GPL-2.0-only AND GPL-2.0-or-later AND LGPL-2.1-or-later AND ((GPL-2.0-or-later OR LGPL-3.0-or-later) OR BSD-3-Clause) AND (MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later)
URL:            https://wiki.gnome.org/Projects/GnomeKeyring
Source0:        https://download.gnome.org/sources/%{name}/46/%{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(gcr-3) >= %{gcr_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(p11-kit-1)
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  libgcrypt-devel >= %{gcrypt_version}
BuildRequires:  libselinux-devel
BuildRequires:  make
BuildRequires:  pam-devel
BuildRequires:  systemd-rpm-macros
%if %{with ssh_agent}
BuildRequires:  /usr/bin/ssh-add
BuildRequires:  /usr/bin/ssh-agent
%endif
BuildRequires:  /usr/bin/xsltproc

%if %{with ssh_agent}
Requires: /usr/bin/ssh-add
Requires: /usr/bin/ssh-agent
%endif
# for /usr/libexec/gcr-ssh-askpass
Requires: gcr3

%description
The gnome-keyring session daemon manages passwords and other types of
secrets for the user, storing them encrypted with a main password.
Applications can use the gnome-keyring library to integrate with the keyring.


%package pam
Summary: Pam module for unlocking keyrings
License: LGPL-2.1-or-later
Requires: %{name}%{?_isa} = %{version}-%{release}
# for /lib/security
Requires: pam%{?_isa}

%description pam
The gnome-keyring-pam package contains a pam module that can
automatically unlock the "login" keyring when the user logs in.


%prep
%autosetup -p1


%build
%configure \
           --with-pam-dir=%{_libdir}/security \
           --enable-pam \
           --with-systemd \
           --without-libcap-ng \
           --with-pkcs11-config=%{_datadir}/p11-kit/modules \
%if %{with ssh_agent}
           --enable-ssh-agent
%else
           --disable-ssh-agent
%endif

# avoid unneeded direct dependencies
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

%make_build


%install
%make_install

rm $RPM_BUILD_ROOT%{_libdir}/security/*.la
rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gnome-keyring/devel/*.la

%find_lang gnome-keyring

%post
%systemd_user_post gnome-keyring-daemon.service

%preun
%systemd_user_preun gnome-keyring-daemon.service

%files -f gnome-keyring.lang
%doc AUTHORS NEWS README
%license COPYING COPYING.LIB
# LGPL
%dir %{_libdir}/gnome-keyring
%dir %{_libdir}/gnome-keyring/devel
%{_libdir}/gnome-keyring/devel/*.so
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/*.so
# GPL
%{_bindir}/gnome-keyring-daemon
%{_bindir}/gnome-keyring
%{_bindir}/gnome-keyring-3
%{_datadir}/dbus-1/services/*.service
%{_sysconfdir}/xdg/autostart/*
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/p11-kit/modules/gnome-keyring.module
%dir %{_datadir}/xdg-desktop-portal
%dir %{_datadir}/xdg-desktop-portal/portals
%{_datadir}/xdg-desktop-portal/portals/gnome-keyring.portal
%{_mandir}/man1/gnome-keyring.1*
%{_mandir}/man1/gnome-keyring-3.1*
%{_mandir}/man1/gnome-keyring-daemon.1*
%{_userunitdir}/gnome-keyring-daemon.service
%{_userunitdir}/gnome-keyring-daemon.socket

%files pam
%{_libdir}/security/*.so


%autochangelog
