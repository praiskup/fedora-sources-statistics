%global gimpplugindir %(%___build_pre; gimptool --gimpplugindir)/plug-ins

%global use_system_cimg 1

# As generated by new-snapshot.sh script
%global zart_version 20231127gitd014169
%global gmic_qt_version 20240903gitaa4a6f4
%global gmic_community_version 20241013git29117687


Summary: GREYC's Magic for Image Computing
Name:    gmic
Version: 3.4.3
%global shortver %(foo=%{version}; echo ${foo//./})
Release: 2%{?dist}
Source0: https://gmic.eu/files/source/%{name}_%{version}.tar.gz
# GIT archive snapshot of https://github.com/c-koi/zart
Source1: zart-%{zart_version}.tar.gz
# GIT archive snapshot of https://github.com/c-koi/gmic-qt
Source2: gmic-qt-%{gmic_qt_version}.tar.gz
# GIT archive snapshot of https://github.com/dtschump/gmic-community
Source3: gmic-community-%{gmic_community_version}.tar.gz

# Taken from https://github.com/c-koi/gmic-qt/pull/208
#Patch1: 0001-Host-Gimp-replace-GIMP_VERSION_LTE-with-GIMP_CHECK_V.patch
#Patch2: 0002-Host-Gimp-stop-open-coding-version-checks.patch
#Patch3: 0003-Host-Gimp-convert-to-new-GimpProcedureConfig-APIs.patch

License: ( CECILL-2.1 OR CECILL-C ) AND GPL-3.0-or-later
Url: http://gmic.eu/
%if %{use_system_cimg}
BuildRequires: CImg-devel == 1:%{version}
%endif
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libtiff-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: fftw-devel
%if 0%{?fedora} > 34
BuildRequires: openexr-devel
BuildRequires: imath-devel
%else
BuildRequires: OpenEXR-devel
BuildRequires: ilmbase-devel
%endif
BuildRequires: zlib-devel
BuildRequires: gimp-devel-tools
BuildRequires: hdf5-devel
BuildRequires: opencv-devel
BuildRequires: GraphicsMagick-c++-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-linguist
BuildRequires: libcurl-devel
BuildRequires: gcc-c++
BuildRequires: desktop-file-utils
BuildRequires: make
BuildRequires: chrpath

Provides: bundled(zart) = %{zart_version}
Provides: bundled(gmic-qt) = %{gmic_qt_version}
Provides: bundled(gmic-community) = %{gmic_community_version}

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

# The C library binding was mistakenly put in a -static
# package despite being a shared library
Obsoletes:     gmic-static <= 2.1.8
# we no longer have gimp-devel-tools on s390x
ExcludeArch:    s390x

%description
G'MIC is an open and full-featured framework for image processing, providing
several different user interfaces to convert/manipulate/filter/visualize
generic image datasets, from 1d scalar signals to 3d+t sequences of
multi-spectral volumetric images.

%package devel
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Summary: Development files for G'MIC

%package gimp
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: G'MIC plugin for GIMP

%package libs
Summary: G'MIC shared libraries

%description devel
G'MIC is an open and full-featured framework for image processing, providing
several different user interfaces to convert/manipulate/filter/visualize
generic image datasets, from 1d scalar signals to 3d+t sequences of
multi-spectral volumetric images.

Provides files for building applications against the G'MIC API

%description gimp
G'MIC is an open and full-featured framework for image processing, providing
several different user interfaces to convert/manipulate/filter/visualize
generic image datasets, from 1d scalar signals to 3d+t sequences of
multi-spectral volumetric images.

Provides a plugin for using G'MIC from GIMP

%description libs
G'MIC is an open and full-featured framework for image processing, providing
several different user interfaces to convert/manipulate/filter/visualize
generic image datasets, from 1d scalar signals to 3d+t sequences of
multi-spectral volumetric images.

Provides G'MIC shared libraries

%prep
%setup -q -a 1 -a 3

# gmic bundles 'qt', but we don't assume they have the latest
# version, so remove it and provide our own
rm -rf gmic-qt
tar zxvf %{SOURCE2}

cd gmic-qt
# no longer needed
#%%patch 1 -p1
#%%patch 2 -p1
#%%patch 3 -p1

# remove stash-file (thanks Wolfgang Lieff <Wolfgang.Lieff@airborneresearch.org.au>)
rm -f zart/.qmake.stash

%build
# ccache can be used only in local builds, koji and copr don't use it
#export CCACHE_DISABLE=1
cd src

ln -fs ../gmic-community/libcgmic/gmic_libc.cpp .
ln -fs ../gmic-community/libcgmic/gmic_libc.h .
ln -fs ../gmic-community/libcgmic/use_libcgmic.c .

%if %{use_system_cimg}
# We want to build against the system installed CImg package.
# G'MIC provides no way todo this, so we just copy the file
# over what's there already
mv CImg.h CImg.h.bak
cp /usr/include/CImg.h CImg.h
%endif

make OPT_CFLAGS="%{optflags} -g" NOSTRIP=1 PREFIX=%{_prefix} LIB=%{_lib} cli lib libc

cd ../gmic-qt
%{qmake_qt5} CONFIG+=release GMIC_PATH=../src HOST=gimp3 gmic_qt.pro && %{make_build}
%{qmake_qt5} CONFIG+=release GMIC_PATH=../src HOST=none gmic_qt.pro && %{make_build}

cd ../zart
%{qmake_qt5} CONFIG+=release GMIC_PATH=../src zart.pro && %{make_build}

%install
mv gmic-qt/COPYING COPYING-gmic-qt
mv gmic-community/libcgmic/COPYING COPYING-libcgmic


iconv -f iso8859-1 -t utf-8 COPYING > COPYING.conv && mv -f COPYING.conv COPYING
iconv -f iso8859-1 -t utf-8 COPYING-libcgmic > COPYING-libcgmic.conv && mv -f COPYING-libcgmic.conv COPYING-libcgmic

cd src
# Makefile hardcodes gimptool-2.0 for setting PLUGIN var, so
# override for gimp-3 compat until upstream fixes its rules
make DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIB=%{_lib} PLUGIN=%{gimpplugindir} install

desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/gmic_qt.desktop
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/zart.desktop

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mv $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions/gmic $RPM_BUILD_ROOT/%{_sysconfdir}/bash_completion.d/gmic
rm -rf $RPM_BUILD_ROOT/%{_datadir}/bash-completion/completions/

# Sourced files shouldn't be executable
chmod -x $RPM_BUILD_ROOT/%{_sysconfdir}/bash_completion.d/gmic

# remove rpaths
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gmic
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libcgmic.so.%{shortver}
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgmic.so.%{shortver}

%ldconfig_scriptlets libs

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README
%license COPYING COPYING-gmic-qt COPYING-libcgmic
%{_bindir}/gmic
%{_bindir}/gmic_qt
%{_bindir}/zart
%{_sysconfdir}/bash_completion.d/gmic
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/fr/man1/%{name}.1.gz
%{_datadir}/applications/gmic_qt.desktop
%{_datadir}/applications/zart.desktop
%{_datadir}/icons/hicolor/48x48/apps/gmic_qt.png
%{_datadir}/icons/hicolor/48x48/apps/zart.png
%{_datadir}/icons/hicolor/scalable/apps/gmic_qt.svg
%{_datadir}/icons/hicolor/scalable/apps/zart.svg

%files devel
%{_prefix}/include/gmic.h
%{_prefix}/include/gmic_libc.h
%{_libdir}/libgmic.so
%{_libdir}/libcgmic.so

%files gimp
%{gimpplugindir}/gmic_gimp_qt
%{_datadir}/gmic/gmic_cluts.gmz
%{_datadir}/gmic/gmic_denoise_cnn.gmz
%{_datadir}/gmic/gmic_fonts.gmz
%{_datadir}/gmic/gmic_lightleaks.gmz

%files libs
%license COPYING COPYING-libcgmic
%{_libdir}/libgmic.so.3*
%{_libdir}/libcgmic.so.3*

%changelog
* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 3.4.3-2
- Rebuild for hdf5 1.14.5

* Mon Oct 14 2024 josef radinger <cheese@nosuchhost.net> - 3.4.3-1
- bump version

* Thu Sep 12 2024 josef radinger <cheese@nosuchhost.net> - 3.4.2-5
- missed the release being still on -4
- Patch3: 0003-Host-Gimp-convert-to-new-GimpProcedureConfig-APIs.patch no longer needed


* Thu Sep 12 2024 josef radinger <cheese@nosuchhost.net> - 3.4.2-1
- bump version
- Patch1: 0001-Host-Gimp-replace-GIMP_VERSION_LTE-with-GIMP_CHECK_V.patch no longer be needed
- Patch2: 0002-Host-Gimp-stop-open-coding-version-checks.patch no longer needed

* Thu Aug 29 2024 Daniel P. Berrangé <berrange@redhat.com> - 3.4.0-4
- Update to new versions
- Fix GIMP 2.99.19 compat

* Thu Jul 25 2024 Sérgio Basto <sergio@serjux.com> - 3.4.0-3
- Rebuild for opencv 4.10.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 josef radinger <cheese@nosuchhost.net> - 3.4.0-1
- bump version

* Fri May 31 2024 Sérgio Basto <sergio@serjux.com> - 3.3.6-1
- Update gmic to 3.3.6 (#2083488)

* Wed May 08 2024 Sérgio Basto <sergio@serjux.com> - 3.3.5-1
- Update gmic to 3.3.5 (#2083488)

* Wed Apr 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.3.1-5
- Rebuilt for openexr 3.2.4

* Mon Feb 05 2024 Sérgio Basto <sergio@serjux.com> - 3.3.1-4
- Rebuild for opencv 4.9.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 josef radinger <cheese@nosuchhost.net> - 3.3.1-1
- bump version

* Mon Aug 07 2023 Sérgio Basto <sergio@serjux.com> - 3.2.6-3
- Rebuild for opencv 4.8.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 26 2023 josef radinger <cheese@nosuchhost.net> - 3.2.6-1
- bump version

* Tue May 30 2023 josef radinger <cheese@nosuchhost.net> - 3.2.5-1
- bump version

* Mon May 22 2023 josef radinger <cheese@nosuchhost.net> - 3.2.4-1
- bump version
- remove Patch3
- adjust rpath removal

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Sérgio Basto <sergio@serjux.com> - 3.1.6-3
- Rebuild for opencv 4.7.0

* Sun Nov 13 2022 josef radinger <cheese@nosuchhost.net> - 3.1.6-2
- build

* Tue Nov 08 2022 Sérgio Basto <sergio@serjux.com> - 3.1.6-1
- Update to 3.1.6

* Sun Oct 09 2022 Kalev Lember <klember@redhat.com> - 3.1.0-5
- Split out gmic-libs to a subpackage

* Wed Sep 07 2022 Kalev Lember <klember@redhat.com> - 3.1.0-4
- Clean up multilib path install

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Sérgio Basto <sergio@serjux.com> - 3.1.0-2
- Rebuilt for opencv 4.6.0

* Thu Apr 28 2022 josef radinger <cheese@nosuchhost.net> - 3.1.0-1
- bump version
- disable patch0
- disable patch2
- BuildRequires: chrpath

* Wed Jan 26 2022 josef radinger <cheese@nosuchhost.net> - 3.0.2-1
- bump version

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 josef radinger <cheese@nosuchhost.net> -3.0.1-1
- bump version
- add gmic_denoise_cnn.gmz to gimp-subpackage

* Sat Dec 11 2021 josef radinger <cheese@nosuchhost.net> -3.0.0-1
- bump version

* Thu Nov 25 2021 Orion Poplawski <orion@nwra.com> - 2.9.9-2
- Rebuild for hdf5 1.12.1

* Mon Sep 06 2021 josef radinger <cheese@nosuchhost.net> - 2.9.9-1
- bump version

* Sat Aug 21 2021 Richard Shaw <hobbes1069@gmail.com> - 2.9.8-4
- Rebuild for OpenEXR/Imath 3.1.

* Sat Jul 31 2021 Richard Shaw <hobbes1069@gmail.com> - 2.9.8-3
- Rebuild with OpenEXR/Imath 3.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 josef radinger <cheese@nosuchhost.net> - 2.9.8-1
- bump version

* Fri Apr 09 2021 josef radinger <cheese@nosuchhost.net> - 2.9.7-1
- bump version

* Thu Feb 11 2021 josef radinger <cheese@nosuchhost.net> - 2.9.6-1
- bump version

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-5
- Again try to build on all archs

* Tue Jan 12 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-4
- Once make this package available on buildable arch

* Mon Jan 04 2021 josef radinger <cheese@nosuchhost.net> - 2.9.4-3
- remove stray stash file

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 2.9.4-2
- Rebuild for OpenEXR 2.5.3.

* Tue Nov 24 2020 josef radinger <cheese@nosuchhost.net> - 2.9.4-1
- bump version

* Thu Nov 19 2020 josef radinger <cheese@nosuchhost.net> - 2.9.3-1
- bump version

* Thu Oct 22 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.9.2-4
- Rebuilt for OpenCV

* Tue Sep 08 2020 josef radinger <cheese@nosuchhost.net> - 2.9.2-3
- we now have desktop-files

* Tue Sep 08 2020 josef radinger <cheese@nosuchhost.net> - 2.9.2-1
- bump version

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 12 2020 josef radinger <cheese@nosuchhost.net> - 2.9.1-2
- rebuild

* Fri Jun 12 2020 josef radinger <cheese@nosuchhost.net> - 2.9.1-1
- bump version
- remove patch1 (for new opencv)

* Thu Jun 04 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.9.0-4
- Rebuilt for OpenCV 4.3

* Thu Apr 2 2020 josef radinger <cheese@nosuchhost.net> - 2.9.0-3
- enable mtune on aarch64

* Thu Apr 2 2020 josef radinger <cheese@nosuchhost.net> - 2.9.0-2
- disable mtune=generic for s390x, armv7hl and ppc64le

* Mon Mar 30 2020 josef radinger <cheese@nosuchhost.net> - 2.9.0-1
- bump version
- update gmic_opencv.patch

* Thu Feb 13 2020 josef radinger <cheese@nosuchhost.net> - 2.8.4-1
- bump version

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 28 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.8.3-2
- Rebuild for OpenCV 4.2

* Fri Jan 24 2020 josef radinger <cheese@nosuchhost.net> - 2.8.3-1
- bump version

* Wed Jan 15 2020 josef radinger <cheese@nosuchhost.net> - 2.8.2-1
- bump version

* Sun Dec 29 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.7.4-4
- Rebuilt for opencv4

* Fri Oct 18 2019 josef radinger <cheese@nosuchhost.net> - 2.7.4-3
- add patch for building against opencv 4.1.2

* Fri Oct 18 2019 josef radinger <cheese@nosuchhost.net> - 2.7.4-2
- rebuild against opencv 4.1.2

* Tue Oct 15 2019 josef radinger <cheese@nosuchhost.net> - 2.7.4-1
- bump version

* Wed Sep 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7.0-2
- Rebuild for opencv (with vtk disabled)

* Thu Aug 15 2019 josef radinger <cheese@nosuchhost.net> - 2.7.0-1
- bump version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 josef radinger <cheese@nosuchhost.net> - 2.6.6-1
- bump version

* Tue May 28 2019 josef radinger <cheese@nosuchhost.net> - 2.6.4-1
- bump version

* Thu Apr 18 2019 josef radinger <cheese@nosuchhost.net> - 2.5.7-1
- bump version

* Thu Apr 11 2019 Richard Shaw <hobbes1069@gmail.com> - 2.5.6-2
- Rebuild for OpenEXR/Ilmbase 2.3.0.
- Move licences files to %%license.

* Mon Apr 08 2019 josef radinger <cheese@nosuchhost.net> - 2.5.6-1
- bump version

* Sat Mar 30 2019 josef radinger <cheese@nosuchhost.net> - 2.5.5-1
- bump version

* Sun Mar 24 2019 josef radinger <cheese@nosuchhost.net> - 2.5.4-1
- bump version

* Mon Mar 18 2019 Orion Poplawski <orion@nwra.com> - 2.5.3-2
- Rebuild for hdf5 1.10.5

* Sun Mar 17 2019 josef radinger <cheese@nosuchhost.net> - 2.5.3-1
- bump version
- use gmic_cluts.gmz instead of gmic_film_cluts.gmz

* Sat Mar 16 2019 josef radinger <cheese@nosuchhost.net> - 2.5.2-1
- bump version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 josef radinger <cheese@nosuchhost.net> - 2.4.5-1
- bump version
- create %%{_sysconfdir}/bash_completion.d and move the file

* Tue Oct 16 2018 Daniel P. Berrangé <berrange@redhat.com> - 2.4.0-1
- Update to 2.4.0 release

* Tue Sep  4 2018 Daniel P. Berrangé <berrange@redhat.com> - 2.3.6-1
- Update to 2.3.6 release
- Drop BuildRoot and Group tags
- Use system CImg
- Update URL tag

* Mon Jul 23 2018 Daniel P. Berrangé <berrange@redhat.com> - 2.3.3-1
- Updated to latest release / snapshots
- Add BR on gcc-c++

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 05 2018 Adam Williamson <awilliam@redhat.com> - 2.2.0-2
- Rebuild for opencv soname bump

* Thu Feb 22 2018 Daniel P. Berrange <berrange@redhat.com> - 2.2.0-1
- Update to new 2.2.0 upstream release
- Some parts now licensed under choice of CeCILL or CeCILL-C

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Daniel P. Berrange <berrange@redhat.com> - 2.1.8-1
- Update to new 2.1.8 upstream release
- Remove bogus -static sub-RPM which contained shared libs

* Thu Jan 04 2018 josef radinger <cheese@nosuchhost.net> - 1.7.2-6
- Rebuilt for libopencv

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar  2 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuild due to opencv soname change

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jun 4 2016 josef radinger <cheese@nosuchhost.net> - 1.7.2-1
- bump version

* Sun May 8 2016 josef radinger <cheese@nosuchhost.net> - 1.7.1-2
- rebuild for rawhide

* Fri Apr 29 2016 josef radinger <cheese@nosuchhost.net> - 1.7.1-1
- bump version
- update Patch1
- fix link on libgmic
- remove smp_mflags (because of compile-errors)
- split a *-static package

* Fri Feb 5 2016 josef radinger <cheese@nosuchhost.net> - 1.6.9-1
- bump version
- update Patch1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 7 2015 josef radinger <cheese@nosuchhost.net> - 1.6.8-1
- bump version

* Sat Oct 24 2015 josef radinger <cheese@nosuchhost.net> - 1.6.7-1
- bump version
- new downloadurl

* Tue Oct 13 2015 josef radinger <cheese@nosuchhost.net> - 1.6.6.1-1
- bump version

* Tue Jun 23 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.5.0-1
- Update to 1.6.5.0 release
- Enable zart binary build

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.2.0-1
- Update to 1.6.2.0 release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.6.1.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Mar 20 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.1.0-1
- Update to 1.6.1.0 release

* Fri Feb  6 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.4-1
- Update to 1.6.0.4 release

* Fri Dec 19 2014 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.3-1
- Update to 1.6.0.3 release

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 1.6.0.1-2
- rebuild (openexr), s|qt-devel|qt4-devel|, tighten subpkg deps

* Fri Oct  3 2014 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.1-1
- Update to 1.6.0.1 release

* Mon Aug 25 2014 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.0-1
- Update to 1.6.0.0 release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Daniel P. Berrange <berrange@redhat.com> - 1.5.9.4-1
- Initial Fedora package after review (rhbz #1061801)