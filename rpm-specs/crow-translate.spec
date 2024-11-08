%global appid org.kde.CrowTranslate

Name: crow-translate
Version: 3.1.0
Release: %autorelease
Summary: A simple and lightweight translator

# The entire source code is GPL-3.0-only except bundled libs:
# GPL-3.0-or-later: qonlinetranslator
# BSD-3-Clause:     qhotkey
#                   qtaskbarcontrol
#                   singleapplication
# MIT:              singleapplication
License: GPL-3.0-only AND GPL-3.0-or-later AND BSD-3-Clause AND MIT
URL: https://apps.kde.org/crowtranslate/
Source: https://download.kde.org/%{stable_kf5}/%{name}/%{version}/%{name}-v%{version}.tar.gz

BuildRequires: cmake >= 3.16
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: cmake(KF5Wayland)
BuildRequires: cmake(leptonica)
BuildRequires: cmake(Qt5)
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: cmake(tesseract) >= 4.0

Requires: hicolor-icon-theme

Recommends: gstreamer-plugins-good

# Consider submodules in this repo as a way to avoid copy-pasting the code
# https://github.com/crow-translate/crow-translate/issues/615#issuecomment-1762779870
Provides: bundled(qonlinetranslator)
Provides: bundled(qhotkey)
Provides: bundled(qtaskbarcontrol)
Provides: bundled(singleapplication)

%description
Crow Translate is a simple and lightweight translator written in C++ / Qt that
allows you to translate and speak text using Google, Yandex, Bing,
LibreTranslate and Lingva translate API. You may also be interested in my
library QOnlineTranslator used in this project.


%prep
%autosetup -p1 -n %{name}-v%{version}
# Unbundle
#   * Used only on Windows
rm -r src/qgittag


%build
# https://github.com/crow-translate/crow-translate/issues/615#issuecomment-1762934229
# Statically link bundled modules
#   Problem: conflicting requests
#    - nothing provides libQTaskbarControl.so()(64bit) needed by crow-translate-2.10.10-1.fc39.x86_64
#    - nothing provides libqhotkey.so.1()(64bit) needed by crow-translate-2.10.10-1.fc39.x86_64
%{cmake_kf5} \
    -DBUILD_SHARED_LIBS:BOOL=OFF
%cmake_build


%install
%cmake_install
%find_lang %{name} --with-qt


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%license LICENSES/*
%doc README.md
%{_bindir}/crow
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg
%{_metainfodir}/%{appid}.metainfo.xml


%changelog
%autochangelog
