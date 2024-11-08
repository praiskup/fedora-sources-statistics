%global uuid    im.srain.Srain

Name:           srain
Version:        1.7.0
Release:        %autorelease
Summary:        Modern, beautiful IRC client written in GTK+ 3

# The entire source code is GPL-3.0-or-later except:
#   * keypair/      which is BSD-2-Clause
#   * sui_side_bar/ which is GPL-2.0-or-later
License:        GPL-3.0-or-later AND BSD-2-Clause AND GPL-2.0-or-later
URL:            https://github.com/SrainApp/srain
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 0.47
BuildRequires:  python3-sphinx

BuildRequires:  pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.22.15
BuildRequires:  pkgconfig(libconfig) >= 1.5
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(openssl)

Requires:       hicolor-icon-theme

Suggests:       %{name}-doc

%description
%{summary}.


%package doc
Summary:        Documentation files for %{name}
BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description doc
Documentation files for %{name}.


%prep
%autosetup


%build
%meson \
    -Ddoc_builders=html,man
%meson_build


%install
%meson_install
%find_lang %{name}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%doc README.rst
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_mandir}/*1/*.1*
%{_metainfodir}/*.xml
%{_sysconfdir}/%{name}

%files doc
%{_docdir}/%{name}/html/


%changelog
%autochangelog
