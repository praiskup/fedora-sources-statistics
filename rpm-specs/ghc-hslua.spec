# generated by cabal-rpm-2.2.1 --subpackage
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Haskell/

%bcond_with system_lua

%global pkg_name hslua
%global pkgver %{pkg_name}-%{version}
%{?haskell_setup}

%global hsluaaeson hslua-aeson-2.3.1.1
%global hsluaclasses hslua-classes-2.3.1
%global hsluacore hslua-core-2.3.2
%global hsluamarshalling hslua-marshalling-2.3.1
%global hsluaobjectorientation hslua-objectorientation-2.3.1
%global hsluapackaging hslua-packaging-2.3.1
%global hsluatyping hslua-typing-0.1.1
%global lua_hs lua-2.3.2

%global subpkgs %{lua_hs} %{hsluacore} %{hsluamarshalling} %{hsluatyping} %{hsluaobjectorientation} %{hsluapackaging} %{hsluaclasses} %{hsluaaeson}

# testsuite missing deps: lua-arbitrary quickcheck-instances tasty-hslua

Name:           ghc-%{pkg_name}
Version:        2.3.1
# can only be reset when all subpkgs bumped
Release:        1%{?dist}
Summary:        Bindings to Lua, an embeddable scripting language

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
# Begin cabal-rpm sources:
Source0:        https://hackage.haskell.org/package/%{pkgver}/%{pkgver}.tar.gz
Source1:        https://hackage.haskell.org/package/%{hsluaaeson}/%{hsluaaeson}.tar.gz
Source2:        https://hackage.haskell.org/package/%{hsluaclasses}/%{hsluaclasses}.tar.gz
Source3:        https://hackage.haskell.org/package/%{hsluacore}/%{hsluacore}.tar.gz
Source4:        https://hackage.haskell.org/package/%{hsluamarshalling}/%{hsluamarshalling}.tar.gz
Source5:        https://hackage.haskell.org/package/%{hsluaobjectorientation}/%{hsluaobjectorientation}.tar.gz
Source6:        https://hackage.haskell.org/package/%{hsluapackaging}/%{hsluapackaging}.tar.gz
Source7:        https://hackage.haskell.org/package/%{hsluatyping}/%{hsluatyping}.tar.gz
Source8:        https://hackage.haskell.org/package/%{lua_hs}/%{lua_hs}.tar.gz
# End cabal-rpm sources

# Begin cabal-rpm deps:
BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros-extra
BuildRequires:  ghc-base-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-exceptions-devel
#BuildRequires:  ghc-hslua-aeson-devel
#BuildRequires:  ghc-hslua-classes-devel
#BuildRequires:  ghc-hslua-core-devel
#BuildRequires:  ghc-hslua-marshalling-devel
#BuildRequires:  ghc-hslua-objectorientation-devel
#BuildRequires:  ghc-hslua-packaging-devel
#BuildRequires:  ghc-hslua-typing-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-text-devel
%if %{with ghc_prof}
BuildRequires:  ghc-base-prof
BuildRequires:  ghc-bytestring-prof
BuildRequires:  ghc-containers-prof
BuildRequires:  ghc-exceptions-prof
#BuildRequires:  ghc-hslua-aeson-prof
#BuildRequires:  ghc-hslua-classes-prof
#BuildRequires:  ghc-hslua-core-prof
#BuildRequires:  ghc-hslua-marshalling-prof
#BuildRequires:  ghc-hslua-objectorientation-prof
#BuildRequires:  ghc-hslua-packaging-prof
#BuildRequires:  ghc-hslua-typing-prof
BuildRequires:  ghc-mtl-prof
BuildRequires:  ghc-text-prof
%endif
# for missing dep 'hslua-aeson':
BuildRequires:  ghc-aeson-devel
BuildRequires:  ghc-hashable-devel
BuildRequires:  ghc-scientific-devel
BuildRequires:  ghc-unordered-containers-devel
BuildRequires:  ghc-vector-devel
%if %{with ghc_prof}
BuildRequires:  ghc-aeson-prof
BuildRequires:  ghc-hashable-prof
BuildRequires:  ghc-scientific-prof
BuildRequires:  ghc-unordered-containers-prof
BuildRequires:  ghc-vector-prof
%endif
# End cabal-rpm deps
%if %{with system_lua}
BuildRequires:  lua-devel
%else
Provides:       bundled(lua) = 5.4.4
%endif

%description
HsLua provides wrappers and helpers to bridge Haskell and Lua.

It builds upon the lua package, which allows to bundle a Lua interpreter
with a Haskell program.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name}-static%{?_isa} = %{version}-%{release}
%if %{defined ghc_version}
Requires:       ghc-compiler = %{ghc_version}
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if %{with system_lua}
Requires:       lua-devel%{?_isa}
%endif

%description devel
This package provides the Haskell %{pkg_name} library development files.


%if %{with haddock}
%package doc
Summary:        Haskell %{pkg_name} library documentation
BuildArch:      noarch
Requires:       ghc-filesystem

%description doc
This package provides the Haskell %{pkg_name} library documentation.
%endif


%if %{with ghc_prof}
%package prof
Summary:        Haskell %{pkg_name} profiling library
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Supplements:    (%{name}-devel and ghc-prof)

%description prof
This package provides the Haskell %{pkg_name} profiling library.
%endif


%global main_version %{version}

%if %{defined ghclibdir}
%ghc_lib_subpackage -l MIT %{hsluaaeson}
%ghc_lib_subpackage -l MIT %{hsluaclasses}
%ghc_lib_subpackage -l MIT %{hsluacore}
%ghc_lib_subpackage -l MIT %{hsluamarshalling}
%ghc_lib_subpackage -l MIT %{hsluaobjectorientation}
%ghc_lib_subpackage -l MIT %{hsluapackaging}
%ghc_lib_subpackage -l MIT %{hsluatyping}
%ghc_lib_subpackage -l MIT %{lua_hs}
%endif

%global version %{main_version}


%prep
# Begin cabal-rpm setup:
%setup -q -n %{pkgver} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8
# End cabal-rpm setup
%if %{with system_lua}
cabal-tweak-flag system-lua True
rm -r cbits/lua-5.*
%endif


%build
# Begin cabal-rpm build:
%ghc_libs_build %{subpkgs}
%ghc_lib_build
# End cabal-rpm build


%install
# Begin cabal-rpm install
%ghc_libs_install %{subpkgs}
%ghc_lib_install
# End cabal-rpm install


%files -f %{name}.files
# Begin cabal-rpm files:
%license LICENSE
# End cabal-rpm files


%files devel -f %{name}-devel.files
%doc CHANGELOG.md README.md


%if %{with haddock}
%files doc -f %{name}-doc.files
%license LICENSE
%endif


%if %{with ghc_prof}
%files prof -f %{name}-prof.files
%endif


%changelog
* Sun Jul 28 2024 Jens Petersen <petersen@redhat.com> - 2.3.1-1
- https://hackage.haskell.org/package/hslua-2.3.1/changelog

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jul 23 2023 Jens Petersen <petersen@redhat.com> - 2.3.0-3
- https://hackage.haskell.org/package/hslua-2.3.0/changelog

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 26 2023 Jens Petersen <petersen@redhat.com> - 2.2.1-1
- https://hackage.haskell.org/package/hslua-2.2.1/changelog
- refresh to cabal-rpm-2.1.0 with SPDX migration

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 07 2022 Jens Petersen <petersen@redhat.com> - 1.3.0.2-1
- https://hackage.haskell.org/package/hslua-1.3.0.2/changelog

* Thu Mar 10 2022 Jens Petersen <petersen@redhat.com> - 1.3.0.1-3
- rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug  5 2021 Jens Petersen <petersen@redhat.com> - 1.3.0.1-1
- update to 1.3.0.1

* Thu Aug  5 2021 Jens Petersen <petersen@redhat.com> - 1.2.0-1
- update to 1.2.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Jens Petersen <petersen@redhat.com> - 1.0.3.2-2
- used bundled lua-5.3.5 (can't build with lua-5.4)

* Fri Feb 14 2020 Jens Petersen <petersen@redhat.com> - 1.0.3.2-1
- update to 1.0.3.2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Jens Petersen <petersen@redhat.com> - 1.0.3.1-1
- update to 1.0.3.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Jens Petersen <petersen@redhat.com> - 0.9.5.2-3
- refresh to cabal-rpm-0.13

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 22 2018 Jens Petersen <petersen@redhat.com> - 0.9.5.2-1
- update to 0.9.5.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Jens Petersen <petersen@redhat.com> - 0.9.5-1
- update to 0.9.5

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 24 2017 Jens Petersen <petersen@redhat.com> - 0.4.1-3
- refresh to cabal-rpm-0.11.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 23 2016 Jens Petersen <petersen@redhat.com> - 0.4.1-1
- update to 0.4.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 0.3.13-1
- update to 0.3.13

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 0.3.10-2
- hslua needs lua-5.1 so build with compat-lua

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 0.3.10-1
- update to 0.3.10 (#1009375)
- update license to MIT (#1009375)
  see https://github.com/osa1/hslua/issues/14
- system-lua patch is now upstream
- tweak summary and description

* Wed Oct 16 2013 Jens Petersen <petersen@redhat.com> - 0.3.6.1-2
- add static provides to devel

* Wed Sep 18 2013 Jens Petersen <petersen@redhat.com> - 0.3.6.1-1
- summary and description
- patch to use system lua

* Wed Sep 18 2013 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 0.3.6.1-0
- spec file generated by cabal-rpm-0.8.3