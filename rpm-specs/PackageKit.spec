%global glib2_version 2.62.0
%global libdnf_version 0.43.1

Summary:   Package management service
Name:      PackageKit
Version:   1.2.8
Release:   %autorelease
License:   GPL-2.0-or-later AND LGPL-2.1-or-later AND FSFAP
URL:       http://www.freedesktop.org/software/PackageKit/
Source0:   http://www.freedesktop.org/software/PackageKit/releases/%{name}-%{version}.tar.xz

%if 0%{?fedora}
Patch0:    PackageKit-0.3.8-Fedora-Vendor.conf.patch
%elif 0%{?rhel}
Patch0:    PackageKit-0.3.8-RHEL-Vendor.conf.patch
%endif

# https://pagure.io/fedora-workstation/issue/233
# https://github.com/PackageKit/PackageKit/pull/404
Patch1:    package-remove-password-prompt.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=2283063
Patch2:    appstream-mark-pk-as-compulsory.patch

BuildRequires: docbook-utils
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: meson
BuildRequires: vala
BuildRequires: xmlto
BuildRequires: pkgconfig(appstream)
BuildRequires: pkgconfig(bash-completion)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libdnf) >= %{libdnf_version}
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(pangoft2)
BuildRequires: pkgconfig(polkit-gobject-1) >= 0.98
BuildRequires: pkgconfig(sqlite3)
BuildRequires: systemd
BuildRequires: gobject-introspection-devel
BuildRequires: python3-devel

# Validate metainfo
BuildRequires: libappstream-glib

Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: libdnf%{?_isa} >= %{libdnf_version}
Requires: shared-mime-info
Requires: systemd

# functionality moved to udev itself
Obsoletes: PackageKit-udev-helper < %{version}-%{release}
Obsoletes: udev-packagekit < %{version}-%{release}

# No more GTK+-2 plugin
Obsoletes: PackageKit-gtk-module < %{version}-%{release}

# No more zif, smart or yum in Fedora
Obsoletes: PackageKit-smart < %{version}-%{release}
Obsoletes: PackageKit-yum < 0.9.1
Obsoletes: PackageKit-yum-plugin < 0.9.1
Obsoletes: PackageKit-zif < 0.8.13-2

# components now built-in
Obsoletes: PackageKit-debug-install < 0.9.1
Obsoletes: PackageKit-hawkey < 0.9.1
Obsoletes: PackageKit-backend-devel < 0.9.6

# Udev no longer provides this functionality
Obsoletes: PackageKit-device-rebind < 0.8.13-2

%description
PackageKit is a D-Bus abstraction layer that allows the session user
to manage packages in a secure way using a cross-distro,
cross-architecture API.

%package glib
Summary: GLib libraries for accessing PackageKit
Requires: dbus >= 1.1.1
Requires: gobject-introspection
Obsoletes: PackageKit-libs < %{version}-%{release}
Provides: PackageKit-libs = %{version}-%{release}

%description glib
GLib libraries for accessing PackageKit.

%package cron
Summary: Cron job and related utilities for PackageKit
Requires: crontabs
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cron
Crontab and utilities for running PackageKit as a cron job.

%package glib-devel
Summary: GLib Libraries and headers for PackageKit
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: dbus-devel%{?_isa} >= 1.1.1
Requires: sqlite-devel%{?_isa}
Obsoletes: PackageKit-devel < %{version}-%{release}
Provides: PackageKit-devel = %{version}-%{release}
Obsoletes: PackageKit-docs < %{version}-%{release}
Provides: PackageKit-docs = %{version}-%{release}

%description glib-devel
GLib headers and libraries for PackageKit.

%package gstreamer-plugin
Summary: Install GStreamer codecs using PackageKit
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Obsoletes: codeina < 0.10.1-10
Provides: codeina = 0.10.1-10

%description gstreamer-plugin
The PackageKit GStreamer plugin allows any Gstreamer application to install
codecs from configured repositories using PackageKit.

%package gtk3-module
Summary: Install fonts automatically using PackageKit
Requires: pango
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description gtk3-module
The PackageKit GTK3+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%package command-not-found
Summary: Ask the user to install command line programs automatically
Requires: bash
Requires: %{name} = %{version}-%{release}
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description command-not-found
A simple helper that offers to install new packages on the command line
using PackageKit.

%prep
%autosetup -p1

%build
%meson \
        -Dgtk_doc=true \
        -Dpython_backend=false \
        -Dpackaging_backend=dnf \
        -Dlocal_checkout=false
%meson_build

%install
%meson_install

# Create cache dir
mkdir -p %{buildroot}%{_localstatedir}/cache/PackageKit

# Create directories for downloaded appstream data
mkdir -p %{buildroot}%{_localstatedir}/cache/app-info/{icons,xmls}

# create a link that GStreamer will recognise
pushd %{buildroot}%{_libexecdir} > /dev/null
ln -s pk-gstreamer-install gst-install-plugins-helper
popd > /dev/null

%find_lang %name

%check
# FIXME: Validation fails in appstream-util because it does not recognize component type "service"
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml || :

%post
# Remove leftover symlinks from /etc/systemd; the offline update service is
# instead now hooked into /usr/lib/systemd/system/system-update.target.wants
systemctl disable packagekit-offline-update.service > /dev/null 2>&1 || :

%files -f %{name}.lang
%license COPYING
%doc README AUTHORS NEWS
%dir %{_datadir}/PackageKit
%dir %{_sysconfdir}/PackageKit
%dir %{_localstatedir}/lib/PackageKit
%dir %{_localstatedir}/cache/app-info
%dir %{_localstatedir}/cache/app-info/icons
%dir %{_localstatedir}/cache/app-info/xmls
%dir %{_localstatedir}/cache/PackageKit
%{_datadir}/bash-completion/completions/pkcon
%dir %{_libdir}/packagekit-backend
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %{_sysconfdir}/PackageKit/Vendor.conf
%{_datadir}/man/man1/pkcon.1*
%{_datadir}/man/man1/pkmon.1*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/*
%{_datadir}/PackageKit/pk-upgrade-distro.sh
%{_datadir}/PackageKit/helpers/test_spawn/search-name.sh
%{_metainfodir}/org.freedesktop.packagekit.metainfo.xml
%{_libexecdir}/packagekitd
%{_libexecdir}/packagekit-direct
%{_bindir}/pkmon
%{_bindir}/pkcon
%exclude %{_libdir}/libpackagekit*.so.*
%{_libdir}/packagekit-backend/libpk_backend_dummy.so
%{_libdir}/packagekit-backend/libpk_backend_test_*.so
%ghost %verify(not md5 size mtime) %attr(0644,-,-) %{_localstatedir}/lib/PackageKit/transactions.db
%{_datadir}/dbus-1/system.d/*
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/interfaces/*.xml
%{_unitdir}/packagekit-offline-update.service
%{_unitdir}/packagekit.service
%{_unitdir}/system-update.target.wants/
%{_libexecdir}/pk-*offline-update
%{_libexecdir}/packagekit-dnf-refresh-repo
%{_libdir}/packagekit-backend/libpk_backend_dnf.so
%pycached %{python3_sitelib}/dnf-plugins/notify_packagekit.py

%files glib
%{_libdir}/*packagekit-glib2.so.*
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib

%files cron
%config %{_sysconfdir}/cron.daily/packagekit-background.cron
%config(noreplace) %{_sysconfdir}/sysconfig/packagekit-background

%files gstreamer-plugin
%{_libexecdir}/pk-gstreamer-install
%{_libexecdir}/gst-install-plugins-helper

%files gtk3-module
%{_libdir}/gtk-3.0/modules/*.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/*.desktop

%files command-not-found
%{_sysconfdir}/profile.d/*
%{_libexecdir}/pk-command-not-found
%config(noreplace) %{_sysconfdir}/PackageKit/CommandNotFound.conf

%files glib-devel
%{_libdir}/libpackagekit-glib2.so
%{_libdir}/pkgconfig/packagekit-glib2.pc
%dir %{_includedir}/PackageKit
%dir %{_includedir}/PackageKit/packagekit-glib2
%{_includedir}/PackageKit/packagekit-glib*/*.h
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir
%{_datadir}/gtk-doc/html/PackageKit
%{_datadir}/vala/vapi/packagekit-glib2.vapi
%{_datadir}/vala/vapi/packagekit-glib2.deps

%changelog
%autochangelog
