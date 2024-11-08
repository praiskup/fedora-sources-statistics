%bcond_with tests

%global sysname gsecrets
%global oldname gnome-passwordsafe
%global libadwaita_version 1.4.99
%global pykeepass_version 4.0.7
%global pyotp_version 2.4.0

Name:           secrets
Version:        9.6
Release:        %autorelease
Summary:        Manage your passwords

License:        GPL-3.0-only
URL:            https://gitlab.gnome.org/World/secrets
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2
# https://gitlab.gnome.org/World/secrets/-/issues/537
Patch:          https://gitlab.gnome.org/World/secrets/uploads/7634fbc1777cce060724770e7c3a0aff/0001-Open-borked-databases.patch
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 0.59
BuildRequires:  python3-devel >= 3.8
BuildRequires:  python3-yubico

BuildRequires:  python3dist(pykcs11)
BuildRequires:  python3dist(pykeepass) >= %{pykeepass_version}
BuildRequires:  python3dist(pyotp) >= %{pyotp_version}
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(validators)
BuildRequires:  python3dist(zxcvbn)

BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.73.1
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.66
BuildRequires:  pkgconfig(gtk4) >= 4.9
BuildRequires:  pkgconfig(libadwaita-1) >= %{libadwaita_version}

%if %{with tests}
BuildRequires:  python3-gobject
BuildRequires:  python3dist(pytest)
%endif

Requires:       hicolor-icon-theme
Requires:       libadwaita >= %{libadwaita_version}
Requires:       python3-gobject
Requires:       python3-pykcs11
Requires:       python3-pykeepass >= %{pykeepass_version}
Requires:       python3-pyotp >= %{pyotp_version}
Requires:       python3-validators
Requires:       python3-yubico
Requires:       python3-zxcvbn

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} <= 5.1-6

%description
Secrets is a password manager which integrates perfectly with the GNOME
desktop and provides an easy and uncluttered interface for the management of
password databases.

Features:
  * Create or import KeePass safes
  * Assign a color and additional attributes to entries
  * Add attachments to your encrypted database
  * Generate cryptographically strong passwords
  * Change the password or keyfile of your database
  * Quickly search your favorite entries
  * Automatic database lock during inactivity
  * Adaptive interface
  * Support for two-factor authentication


%prep
%autosetup -p1


%build
%meson \
  %if %{with tests}
  -Dtests=true \
  %endif
  %{nil}
%meson_build


%install
%meson_install
%find_lang %{name}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%if %{with tests}
%meson_test
%endif


%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/*/*.svg
%{_datadir}/mime/packages/*.xml
%{_metainfodir}/*.xml
%{python3_sitelib}/%{sysname}/


%changelog
%autochangelog
