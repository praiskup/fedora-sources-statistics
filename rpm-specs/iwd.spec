Name:           iwd
Version:        3.0
Release:        %autorelease
Summary:        Wireless daemon for Linux
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            https://iwd.wiki.kernel.org/
Source0:        https://www.kernel.org/pub/linux/network/wireless/%{name}-%{version}.tar.xz

BuildRequires:  asciidoc
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(ell) >= 0.43
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  python3-docutils
BuildRequires:  readline-devel

Requires:       dbus
Requires:       systemd
Recommends:     wireless-regdb


%description
The daemon and utilities for controlling and configuring the Wi-Fi network
hardware.


%prep
%autosetup -p1


%build
%configure			\
	--enable-external-ell	\
	--enable-sim-hardcoded	\
	--enable-ofono		\
	--enable-wired		\
	--enable-hwsim		\
	--enable-tools		\
	--with-systemd-unitdir=%{_unitdir} \
	--with-systemd-networkdir=%{_systemd_util_dir}/network \
	--with-systemd-modloaddir=%{_modulesloaddir}

%make_build V=1


%install
%make_install
mkdir -p %{buildroot}%{_sharedstatedir}/iwd
mkdir -p %{buildroot}%{_sharedstatedir}/ead

# Don't let iwd adjust interface naming. It would break user configurations.
rm %{buildroot}/usr/lib/systemd/network/80-iwd.link


%files
%license COPYING
%doc AUTHORS ChangeLog
%{_bindir}/iwctl
%{_bindir}/iwmon
%{_bindir}/hwsim
%{_libexecdir}/iwd
%{_libexecdir}/ead
%{_modulesloaddir}/pkcs8.conf
%{_unitdir}/ead.service
%{_unitdir}/iwd.service
%{_datadir}/dbus-1/system-services/net.connman.iwd.service
%{_datadir}/dbus-1/system-services/net.connman.ead.service
%{_datadir}/dbus-1/system.d/iwd-dbus.conf
%{_datadir}/dbus-1/system.d/ead-dbus.conf
%{_datadir}/dbus-1/system.d/hwsim-dbus.conf
%{_mandir}/man*/*
%{_sharedstatedir}/iwd
%{_sharedstatedir}/ead


%changelog
%autochangelog
