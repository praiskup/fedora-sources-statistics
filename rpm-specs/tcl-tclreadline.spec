%{!?tcl_version: %global tcl_version %((echo '8.5'; echo 'puts $tcl_version' | tclsh 2>/dev/null) | tail -1)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%global pkgname tclreadline

Summary:        GNU Readline extension for Tcl/Tk
Name:           tcl-tclreadline
Version:        2.1.0
Release:        25%{?dist}
License:        BSD-3-Clause
URL:            https://tclreadline.sourceforge.net/
Source0:        https://downloads.sourceforge.net/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1:        https://sourceforge.net/p/tclreadline/git/ci/master/tree/sample.tclshrc?format=raw#/sample.tclshrc
Patch0:         tcl-tclreadline-2.1.0-libdir.patch
Patch1:         tcl-tclreadline-2.1.0-syntax.patch
Patch2:         tcl-tclreadline-2.1.0-man-page.patch
Patch3:         tcl-tclreadline-2.1.0-rl_completion.patch
Patch4:         tcl-tclreadline-2.1.0-prompt2.patch
Patch5:         tcl-tclreadline-2.1.0-memuse.patch
Patch6:         tcl-tclreadline-ding.patch
Patch7:         tcl-tclreadline-configure-fclose.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  tcl-devel
BuildRequires:  readline-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
Requires:       tcl(abi) = %{tcl_version}
Provides:       %{pkgname} = %{version}-%{release}
Provides:       %{pkgname}%{?_isa} = %{version}-%{release}

%description
The tclreadline package makes the GNU Readline library available
for interactive tcl shells. This includes history expansion and
file/command completion. Command completion for all tcl/tk commands
is provided and command completion for user defined commands can
be easily added. Tclreadline can also be used for tcl scripts which
want to use a shell like input interface.

%package devel
Summary:        Development files for the tclreadline library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The tclreadline-devel package includes the header file and library
necessary for developing programs which use the tclreadline library.

%prep
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1 -b .libdir
%patch -P1 -p1 -b .syntax
%patch -P2 -p1 -b .man-page
%patch -P3 -p1 -b .rl_completion
%patch -P4 -p1 -b .prompt2
%patch -P5 -p1 -b .memuse
%patch -P6 -p1 -b .ding
%patch -P7 -p1 -b .configure-fclose
autoreconf -f -i

# Copy sample tclshrc for later pickup at %%doc
cp -pf %{SOURCE1} .

%build
%configure --libdir=%{tcl_sitearch}/%{pkgname}%{version} --with-tcl=%{_libdir}

# Avoid unused direct shared library dependency to libncurses
sed -e 's@ -shared @ -Wl,--as-needed\0@g' -i libtool

%make_build

%install
%make_install

# Move the library for linking back to %%{_libdir}
mv -f $RPM_BUILD_ROOT{%{tcl_sitearch}/%{pkgname}%{version},%{_libdir}}/lib%{pkgname}-%{version}.so
rm -f $RPM_BUILD_ROOT%{tcl_sitearch}/%{pkgname}%{version}/lib%{pkgname}.so
ln -s ../../lib%{pkgname}-%{version}.so $RPM_BUILD_ROOT%{tcl_sitearch}/%{pkgname}%{version}/lib%{pkgname}.so
ln -s lib%{pkgname}-%{version}.so $RPM_BUILD_ROOT%{_libdir}/lib%{pkgname}.so

# Remove wrong and unnecessary shebang from files
for file in tclreadlineSetup.tcl tclreadlineInit.tcl pkgIndex.tcl; do
  sed -e '1d' $RPM_BUILD_ROOT%{tcl_sitearch}/%{pkgname}%{version}/$file > \
    $RPM_BUILD_ROOT%{tcl_sitearch}/%{pkgname}%{version}/$file.new
  touch -c -r $RPM_BUILD_ROOT%{tcl_sitearch}/%{pkgname}%{version}/$file{,.new}
  mv -f $RPM_BUILD_ROOT%{tcl_sitearch}/%{pkgname}%{version}/$file{.new,}
done

# Don't install any static .a and libtool .la files
rm -f $RPM_BUILD_ROOT%{tcl_sitearch}/%{pkgname}%{version}/*.{a,la}

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS ChangeLog README sample.tclshrc
%{_libdir}/lib%{pkgname}-%{version}.so
%{tcl_sitearch}/%{pkgname}%{version}
%{_mandir}/mann/%{pkgname}.n*

%files devel
%{_libdir}/lib%{pkgname}.so
%{_includedir}/%{pkgname}.h

%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 18 2022 Florian Weimer <fweimer@redhat.com> - 2.1.0-21
- Fixes for building in strict C99 mode

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.0-13
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Robert Scheck <robert@fedoraproject.org> 2.1.0-3
- Added %%{?_isa} macro to run-time requires/provides
- Escape macros in spec file (#579925, thanks to R P Herrold)

* Sat Jan 01 2011 Robert Scheck <robert@fedoraproject.org> 2.1.0-2
- Renamed package to tcl-tclreadline (#579925 #c1)
- Fixed undefined non-weak symbols by linking tcl (#579925 #c1)

* Tue Apr 06 2010 Robert Scheck <robert@fedoraproject.org> 2.1.0-1
- Upgrade to 2.1.0
- Initial spec file for Fedora and Red Hat Enterprise Linux
