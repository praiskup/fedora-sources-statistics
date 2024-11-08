# This plugin should be noarch but due to the fact that we need the plugin
# installed in libdir we need it to be arch dependent. This makes us to not
# require the debug package.
%global debug_package %{nil}

Name:           gedit-latex
Version:        3.20.0
Release:        %autorelease
Summary:        gedit plugin for composing and compiling LaTeX documents
License:        GPL-2.0-or-later
URL:            http://projects.gnome.org/gedit
Source0:        https://download.gnome.org/sources/gedit-latex/3.20/gedit-latex-%{version}.tar.xz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  python3-devel

Requires:       gedit
Requires:       python3-gobject
Requires:       python3-dbus
Requires:       texlive
# For compiling utilities
Requires:       rubber

Obsoletes:      gedit-plugins-latex < %{version}-%{release}
Provides:       gedit-plugins-latex = %{version}-%{release}

%description
This plugin assists you in composing and compiling LaTeX documents using gedit.


%prep
%autosetup
autoreconf -fiv
sed -i -e '/^#!\/.*bin\/perl/d' latex/util/eps2png.pl
# Fixing the multilib path
# https://sourceforge.net/tracker/index.php?func=detail&aid=2130308&group_id=204144&atid=988428
sed -i -e 's|_CONFIG_FILENAME = "/etc/texmf/texmf.cnf"|_CONFIG_FILENAME = "/usr/share/texlive/texmf-dist/web2c/texmf.cnf"|' latex/latex/environment.py
sed -i -e 's|_DEFAULT_TEXMF_DIR = "/usr/share/texmf-texlive"|_DEFAULT_TEXMF_DIR = "/usr/share/texmf"|' latex/latex/environment.py


%build
%configure --disable-static
%make_build


%install
%make_install
%py_byte_compile %{__python3} %{buildroot}%{_libdir}/gedit/plugins/latex

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc README NEWS
%{_libdir}/gedit/plugins/latex.plugin
%{_libdir}/gedit/plugins/latex/
%{_datadir}/gedit/plugins/latex/
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.latex.gschema.xml

%changelog
%autochangelog
