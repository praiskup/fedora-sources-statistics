Name:           calceph
Version:        4.0.1
Release:        2%{?dist}
Summary:        Astronomical library to access planetary ephemeris files

License:        CECILL-2.0 OR CECILL-B OR CECILL-C
URL:            https://www.imcce.fr/inpop/calceph
Source0:        https://www.imcce.fr/content/medias/recherche/equipes/asd/%{name}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

# Documentation build doesn't work anymore because it relies on several
# sphinx extensions not packaged / not packageable in Fedora
Obsoletes:      calceph-docs < 4.0.0

BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  cmake

%description
This library is designed to access the binary planetary ephemeris files,
such INPOPxx, JPL DExxx and SPICE ephemeris files.


%package        libs
Summary:        %{name} shared libraries
License:        CECILL-2.0 OR CECILL-B OR CECILL-C

%description    libs
Calceph shared libraries.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        fortran-devel
Summary:        Development files for using %{name} Fortran bindings
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
%if 0%{?fedora}
Requires:       gcc-gfortran%{?_isa}
%else
Requires:       gcc-gfortran
%endif

%description    fortran-devel
%{summary}.


%prep
%autosetup -p1


%build
%cmake \
    -DBUILD_SHARED_LIBS=ON

%cmake_build


%install
%cmake_install


%check
%ctest


%files
%{_bindir}/calceph_*


%files      libs
%license COPYING_CECILL_V2.1.LIB COPYING_CECILL_B.LIB COPYING_CECILL_C.LIB
%{_libdir}/libcalceph.so.2
%{_libdir}/libcalceph.so.2.*


%files      devel
%{_libdir}/libcalceph.so
%{_libdir}/cmake/calceph
%{_includedir}/calceph.h


%files      fortran-devel
%{_includedir}/calceph.mod
%{_includedir}/f90calceph.h


%changelog
* Sat Oct 19 2024 Mattia Verga <mattia.verga@proton.me> - 4.0.1-1
- Update to 4.0.1 (fedora#2316258)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 25 2024 Mattia Verga <mattia.verga@proton.me> - 4.0.0-1
- Update to 4.0.0 (fedora#2276370)
- Removed documentation subpackage due to missing required build tools

* Wed Feb 07 2024 Mattia Verga <mattia.verga@proton.me> - 3.5.5-1
- Update to 3.5.5 (fedora#2262750)

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 03 2023 Mattia Verga <mattia.verga@proton.me> - 3.5.4-1
- Update to 3.5.4 (fedora#2252402)

* Sat Sep 09 2023 Mattia Verga <mattia.verga@proton.me> - 3.5.3-2
- Correctly disable static libs building

* Wed Sep 06 2023 Mattia Verga <mattia.verga@proton.me> - 3.5.3-1
- Update to 3.5.3 (fedora#2237641)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Apr 15 2023 Mattia Verga <mattia.verga@proton.me> - 3.5.2-1
- Update to 3.5.2 (fedora#2185865)

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 02 2022 Mattia Verga <mattia.verga@protonmail.com> - 3.5.1-1
- Update to 3.5.1 (fedora#2059202)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Aug 28 2021 Mattia Verga <mattia.verga@protonmail.com> - 3.5.0-1
- Update to 3.5.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 08 2020 Mattia Verga <mattia.verga@protonmail.com> - 3.4.7-2
- Removed hidden files from docdir
- Move Fortran headers to -fortran-devel subpackage

* Fri Nov 6 2020 Mattia Verga <mattia.verga@protonmail.com> - 3.4.7-1
- Update to 3.4.7
- Fix build errors on s390x
- Fix FCFLAGS transmission to fortran compiler
- Enable multi-threading support

* Tue Nov 3 2020 Mattia Verga <mattia.verga@protonmail.com> - 3.4.6-3
- Enable fortran module build

* Sun Nov  1 2020 Mattia Verga <mattia.verga@protonmail.com> - 3.4.6-2
- Split libs subpackage
- Add ldconfig macro for EPEL7 compatibility

* Sun Nov  1 2020 Mattia Verga <mattia.verga@protonmail.com> - 3.4.6-1
- Initial packaging
