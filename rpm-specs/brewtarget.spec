# force out-of-tree build for spec compatibility with older releases
%undefine __cmake_in_source_build

%global forgeurl https://github.com/Brewtarget/brewtarget

%global _description %{expand:
Brewtarget is an open source beer recipe creation tool. It automatically
calculates color, bitterness, and other parameters for you while you drag and
drop ingredients into the recipe. Brewtarget also has many other tools such as
priming sugar calculators, OG correction help, and a unique mash designing tool.
It also can export and import recipes in BeerXML.}

Name:           brewtarget
Version:        3.0.11
Release:        %{autorelease}
Summary:        An open source beer recipe creation tool 🍺
%forgemeta
# BSD-2-Clause: cmake/modules/FindPhonon.cmake
# WTFPL: images/flag* images/bubbles.svg images/convert.svg images/grain2glass.svg
# CC-BY-SA-3.0 OR LGPL-3.0-only: images/edit-copy.png images/document-print-preview.png
#     images/merge.png images/preferences-other.png images/printer.png
#     images/server-database.png images/kbruch.png images/help-contents.png
# LGPL-2.1-only: images/backup.png
License:    GPL-3.0-or-later AND BSD-2-Clause AND WTFPL AND (CC-BY-SA-3.0 OR LGPL-3.0-only) AND LGPL-2.1-only
URL:        %{forgeurl}
Source0:    %{forgesource}
Patch:      fix_boost_requirements.patch

BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel, qt5-qtwebkit-devel, qt5-qtsvg-devel
BuildRequires:  qt5-qtmultimedia-devel, qt5-linguist
BuildRequires:  boost-devel, xerces-c-devel, xalan-c-devel
BuildRequires:  desktop-file-utils
BuildRequires:  meson
BuildRequires:  git-core
BuildRequires:  pandoc
BuildRequires:  xorg-x11-server-Xvfb
Requires:       sqlite

# Stop building for i686
# See: https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

%description %_description

%prep
%autosetup -n %{name}-%{version} -S git
# Crude way of disabling testLogRotation
sed -i -e '/testLogRotation/d' meson.build


%build
%meson
%meson_build


%install
%meson_install


%check
# Run in minimal graphical env (thanks @ankursinha).
# We need to pass the Meson test command as a script to xvfb-run.
cat > mesontest.sh << EOF
#!/bin/sh
mkdir %{_builddir}/%{name}-%{version}/brewtarget-test
export TMPDIR="%{_builddir}/%{name}-%{version}/brewtarget-test"
%meson_test --verbose
EOF
chmod a+x ./mesontest.sh
xvfb-run ./mesontest.sh
desktop-file-validate %buildroot%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/brewtarget*
%{_docdir}/%{name}/*.markdown
%{_docdir}/%{name}/copyright
%doc doc/manual-en.pdf
%license COPYRIGHT COPYING.GPLv3 COPYING.WTFPL

%changelog
%autochangelog