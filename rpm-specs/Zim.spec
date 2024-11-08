Name:           Zim
Version:        0.75.2
Release:        %autorelease
Summary:        Desktop wiki & notekeeper

# Most source code is GPL-2.0-or-later
# ./zim/plugins/pageindex/generictreemodel,.py is LGPL-2.1-or-later
# Some icons are MIT
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
URL:            http://zim-wiki.org/
Source0:        http://www.zim-wiki.org/downloads/zim-%{version}.tar.gz
# Prevent ABRT from triggering on expected errors (rhbz#2213835)
Patch:          https://github.com/zim-desktop-wiki/zim-desktop-wiki/pull/2482.patch
# Improve screenshot on Wayland
Patch:          https://github.com/zim-desktop-wiki/zim-desktop-wiki/pull/2431.patch
# Avoid unhandled exception (and thus crash report) when cancelling template copy
Patch:          https://github.com/zim-desktop-wiki/zim-desktop-wiki/pull/2505.patch
# Skip favicon.ico in tests/attachmentbrowser
Patch:          https://github.com/zim-desktop-wiki/zim-desktop-wiki/pull/2625.patch
# Not needed for multilib
ExcludeArch:    %{ix86}
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  python3-setuptools
BuildRequires:  gtk3, python3-pyxdg
# for tests
BuildRequires:  /usr/bin/xvfb-run
BuildRequires:  glibc-langpack-en

Requires:       python3-gobject
Requires:       gtk3, python3-pyxdg
Recommends:     libappindicator-gtk3

%description
Zim is a WYSIWYG text editor written in Python which aims to bring the
concept of a wiki to your desktop. Every page is saved as a text file with
wiki markup. Pages can contain links to other pages, and are saved
automatically. Creating a new page is as easy as linking to a non-existing
page. Pages are ordered in a hierarchical structure that gives it the look
and feel of an outliner. This tool is intended to keep track of TODO lists
or to serve as a personal scratch book.

%prep
%autosetup -p1 -n zim-%{version}

%build
./setup.py build

%install
rm -rf %{buildroot}
./setup.py install --root=%{buildroot} --skip-build

%find_lang zim

desktop-file-validate %{buildroot}%{_datadir}/applications/zim.desktop

%check
LANG=en_US.UTF-8 xvfb-run ./test.py

%if 0%{?rhel} && 0%{?rhel} <= 7
%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
%endif

%files -f zim.lang
%license LICENSE
%doc *.md contrib/
%{_mandir}/man[13]/*.[13]*
%{_bindir}/*
%{_datadir}/zim/
%{_datadir}/applications/*
%{_datadir}/mime/packages/zim.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/mimetypes/*
# No package in Fedora provides such directories
%{_datadir}/icons/ubuntu-mono-*/
%{python3_sitelib}/zim-*.egg-info
%{python3_sitelib}/zim/
%{_datadir}/metainfo/*

%changelog
%autochangelog
