Name:		mdk
Version:	1.3.0
Release:	%autorelease
Summary:	GNU MIX Development Kit

# Automatically converted from old format: GPLv3+ and GFDL - review is highly recommended.
License:	GPL-3.0-or-later AND LicenseRef-Callaway-GFDL
URL:		http://www.gnu.org/software/mdk/
Source0:	http://ftp.gnu.org/gnu/mdk/v%{version}/%{name}-%{version}.tar.gz
Source1:	mdk.desktop
Patch0:		glib-deprecated.patch

BuildRequires: make
BuildRequires:  gcc
BuildRequires:	guile30-devel
BuildRequires:	libglade2-devel
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	intltool

%package	doc
Summary:	GNU MIX Development Kit Documentation and Samples
BuildArch:	noarch

%description
MDK stands for MIX Development Kit, and provides tools for developing
and executing, in a MIX virtual machine, MIXAL programs.

The MIX is Donald Knuth's mythical computer, described in the first
volume of The Art of Computer Programming, which is programmed using
MIXAL, the MIX assembly language.

MDK includes a MIXAL assembler (mixasm) and a MIX virtual machine
(mixvm) with a command line interface.  In addition, a GTK+ GUI to
mixvm, called gmixvm, is provided; and, in case you are an Emacs guy,
you can try misc/mixvm.el, which allows running mixvm inside an Emacs
GUD buffer.

Using these interfaces, you can debug your MIXAL programs at source
code level, and read/modify the contents of all the components of the
MIX computer (including block devices, which are simulated using the
file system).

%description doc
Samples and documentation for the MDK package.

%prep
%autosetup -p1

%build
autoconf
%configure
%{make_build}

%install
%{make_install}
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
desktop-file-install \
	--dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
	%{SOURCE1}

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README THANKS
%{_bindir}/mixasm
%{_bindir}/mixvm
%{_bindir}/mixguile
%{_datadir}/mdk
%{_infodir}/*
%{_datadir}/applications/mdk.desktop

%files doc
%doc samples doc

%changelog
%autochangelog
