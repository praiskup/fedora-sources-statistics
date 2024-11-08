Name:           texstudio
Version:        4.8.4
Release:        2%{?dist}

Summary:        A feature-rich editor for LaTeX documents
# texstudio binary: GPLv3 due to static linkage of bundled qcodeedit
# texstudio data and image files: GPLv2+
# Automatically converted from old format: GPLv2+ and GPLv3 - review is highly recommended.
License:        GPL-2.0-or-later AND GPL-3.0-only
URL:            https://www.texstudio.org

Source0:        https://github.com/texstudio-org/texstudio#/archive/%{name}-%{version}.tar.gz
Source1:        texstudio.desktop
Patch1:         texstudio-disable-update-check.patch


BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qttools-static
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  hunspell-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  poppler-devel
BuildRequires:  poppler-qt6-devel
BuildRequires:  poppler-cpp-devel
BuildRequires:  qtsingleapplication-qt6-devel
BuildRequires:  qtsinglecoreapplication-qt6-devel
# Not present in EPEL
%if 0%{?fedora}
BuildRequires:  qtermwidget-devel
%endif
BuildRequires:  quazip-qt6-devel
BuildRequires:  zlib-devel

Recommends:     tex(latex)
Recommends:     tex(preview.sty)
Recommends:     tex-dvipng
Requires:       qt6-qtsvg
# Not present in EPEL
%if 0%{?fedora}
Requires:       qtermwidget
%endif
Provides:       bundled(qcodeedit) 
Provides:       texmakerx = %{version}-%{release}
Obsoletes:      texmakerx < 2.2-1
%description
TeXstudio gives you an environment where you can 
easily create and manage LaTeX documents.
It provides modern writing support, like interactive spell checking, 
code folding, syntax highlighting, integrated pdf viewer
and various assistants. 
Also it serves as a starting point from where you can easily run 
all necessary LaTeX tools.

%prep
%setup -q -n %{name}-%{version}

%patch -P 1 -p1 -b .update_check

rm -rf {hunspell,qtsingleapplication,quazip}

%build
%cmake \
%ifnarch %{ix86} x86_64 %{arm}
    -DTEXSTUDIO_ENABLE_CRASH_HANDLER=OFF \
%endif
%cmake_build

%install
%cmake_install

install -Dp -m 0644 utilities/texstudio16x16.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/texstudio.png
install -Dp -m 0644 utilities/texstudio22x22.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/texstudio.png
install -Dp -m 0644 utilities/texstudio32x32.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/texstudio.png
install -Dp -m 0644 utilities/texstudio48x48.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/texstudio.png
install -Dp -m 0644 utilities/texstudio64x64.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/46x46/apps/texstudio.png


rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/{AUTHORS,COPYING,*.desktop,tex*.png}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/utilities/manual/source/CHANGELOG.md
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/{*.dic,*.aff}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/qt_*.qm

%find_lang %{name} --with-qt

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

%files -f %{name}.lang
%{_bindir}/texstudio
%dir %{_datadir}/texstudio/
%{_datadir}/texstudio/*.png
%{_datadir}/texstudio/*.stopWords
%{_datadir}/texstudio/*.stopWords.level2
%{_datadir}/texstudio/de_DE.badWords
%{_datadir}/texstudio/template_*.tex
%{_datadir}/texstudio/template_*.zip
%{_datadir}/texstudio/*.json
%{_datadir}/texstudio/*.js
%{_datadir}/texstudio/th_*.dat
%{_datadir}/texstudio/*.html
%{_datadir}/texstudio/latex2e.css
%{_datadir}/texstudio/_sphinx_design_static/
%{_datadir}/texstudio/_images/*.webp
%{_datadir}/texstudio/_static/
%{_datadir}/texstudio/README_*
%{_datadir}/texstudio/CHANGELOG.md
%{_datadir}/applications/texstudio.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/metainfo/texstudio.metainfo.xml

%doc utilities/AUTHORS utilities/COPYING utilities/manual/source/CHANGELOG.md

%changelog
* Mon Sep 30 2024 Marco Huenseler <marco@wuthoehle.de> 4.8.4-2
- build with qt6 instead of qt5 and update dependencies

* Sat Sep 28 2024 Johannes Lips <hannes@fedoraproject.org> 4.8.4-1
- update to 4.8.4

* Sat Sep 21 2024 Johannes Lips <hannes@fedoraproject.org> 4.8.3-2
- changed dependency to tex(latex) into weak dependency

* Sat Sep 21 2024 Johannes Lips <hannes@fedoraproject.org> 4.8.3-1
- update to 4.8.3

* Wed Aug 28 2024 Johannes Lips <hannes@fedoraproject.org> 4.8.2-1
- update to 4.8.2

* Tue Aug 13 2024 Orion Poplawski <orion@nwra.com> - 4.8.1-4
- Rebuild with qtermwidget 2.0

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 4.8.1-3
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Johannes Lips <hannes@fedoraproject.org> 4.8.1-1
- update to 4.8.1

* Sat May 11 2024 Johannes Lips <hannes@fedoraproject.org> 4.8.0-1
- update to 4.8.0

* Fri Mar 01 2024 Johannes Lips <hannes@fedoraproject.org> 4.7.3-1
- update to 4.7.3

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 25 2023 Johannes Lips <hannes@fedoraproject.org> 4.7.2-1
- update to 4.7.2

* Sat Dec 02 2023 Johannes Lips <hannes@fedoraproject.org> 4.7.0-1
- update to 4.7.0

* Fri Aug 11 2023 Johannes Lips <hannes@fedoraproject.org> 4.6.3-1
- update to 4.6.3

* Fri Aug 04 2023 Johannes Lips <hannes@fedoraproject.org> 4.6.2-1
- update to 4.6.2

* Sun Jul 30 2023 Johannes Lips <hannes@fedoraproject.org> 4.6.1-1
- update to 4.6.1

* Fri Jul 28 2023 Johannes Lips <hannes@fedoraproject.org> 4.6.0-1
- update to 4.6.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 05 2023 Nicolas Chauvet <kwizart@gmail.com> - 4.5.2-3
- Rebuilt for quazip 1.4

* Sat Apr 15 2023 Johannes Lips <hannes@fedoraproject.org> 4.5.2-2
- fixed patch macro
- minor fixes

* Sat Apr 15 2023 Johannes Lips <hannes@fedoraproject.org> 4.5.2-1
- Update to latest upstream release 4.5.2

* Sat Feb 04 2023 Johannes Lips <hannes@fedoraproject.org> 4.5.1-1
- Update to latest upstream release 4.5.1

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 27 2022 Johannes Lips <hannes@fedoraproject.org> 4.4.1-1
- Update to latest upstream release 4.4.1

* Tue Nov 22 2022 Johannes Lips <hannes@fedoraproject.org> 4.4.0-3
- removed patches 

* Tue Nov 22 2022 Johannes Lips <hannes@fedoraproject.org> 4.4.0-2
- switch to cmake build
- build patches are not necessary any more

* Sat Nov 19 2022 Johannes Lips <hannes@fedoraproject.org> 4.4.0-1
- Update to latest upstream release 4.4.0

* Fri Aug 26 2022 Johannes Lips <hannes@fedoraproject.org> 4.3.1-1
- Update to latest upstream release 4.3.1

* Mon Aug 08 2022 Johannes Lips <hannes@fedoraproject.org> 4.3.0-1
- Update to latest upstream release 4.3.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 23 2022 Johannes Lips <hannes@fedoraproject.org> 4.2.3-1
- Update to latest upstream release 4.2.3

* Mon Apr 18 2022 Miro Hrončok <mhroncok@redhat.com> - 4.2.2-2
- Rebuilt for quazip 1.3

* Sun Feb 20 2022 Johannes Lips <hannes@fedoraproject.org> 4.2.2-1
- Update to latest upstream release 4.2.2

* Fri Jan 28 2022 Johannes Lips <hannes@fedoraproject.org> 4.2.1-1
- Update to latest upstream release 4.2.1

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Johannes Lips <hannes@fedoraproject.org> 4.2.0-1
- Update to latest upstream release 4.2.0

* Mon Jan 03 2022 Ian McInerney <ian.s.mcinerney@ieee.org> 4.0.4-2
- Rebuild due to qtermwidget soname bump (fixes rhbz: 2036642)

* Sun Nov 07 2021 Johannes Lips <hannes@fedoraproject.org> 4.0.4-1
- Update to latest upstream release 4.0.4

* Sat Oct 23 2021 Johannes Lips <hannes@fedoraproject.org> 4.0.2-1
- Update to latest upstream release 4.0.2

* Mon Oct 11 2021 Johannes Lips <hannes@fedoraproject.org> 4.0.1-1
- Update to latest upstream release 4.0.1

* Wed Sep 29 2021 Christian Dersch <lupinix@mailbox.org> - 4.0.0-2
- Use quazip-qt5, fix include and linker variables for quazip5

* Sun Sep 26 2021 Johannes Lips <hannes@fedoraproject.org> 4.0.0-1
- Update to latest upstream release 4.0.0

* Thu Aug 19 2021 Björn Esser <besser82@fedoraproject.org> - 3.1.2-3
- Rebuild (quazip)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Johannes Lips <hannes@fedoraproject.org> 3.1.2-1
- Update to latest upstream release 3.1.2

* Mon Feb 22 2021 Johannes Lips <hannes@fedoraproject.org> 3.1.1-1
- Update to latest upstream release 3.1.1

* Wed Feb 17 2021 Johannes Lips <hannes@fedoraproject.org> 3.1.0-1
- Update to latest upstream release 3.1.0

* Tue Feb 16 2021 Johannes Lips <hannes@fedoraproject.org> 3.0.5-1
- Update to latest upstream release 3.0.5

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 03 2021 Johannes Lips <hannes@fedoraproject.org> 3.0.4-2
- fixed runtime requirements for internal terminal

* Sat Jan 02 2021 Johannes Lips <hannes@fedoraproject.org> 3.0.4-1
- Update to latest upstream release 3.0.4
