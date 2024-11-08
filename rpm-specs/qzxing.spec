%if 0%{?fedora} >= 40
%global qtver 6
%else
%global qtver 5
%endif

%global qmake %{expand:%{qmake_qt%{qtver}}}

%global forgeurl    https://github.com/ftylitak/%{name}

Version:        3.3.0

%forgemeta

Name:           qzxing
Release:        %autorelease
Summary:        Qt/QML wrapper library for the ZXing library

License:        Apache-2.0
URL:            %{forgeurl}
Source0:        %{forgesource}

Patch1:         0001-fix-libdir.patch
# https://github.com/ftylitak/qzxing/pull/224
Patch2:         0002-match-badly-printed-QR-codes.patch

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(Qt%{qtver}Core)

# qzxing uses a heavily modified version of zxing
Provides:       bundled(zxing)

%description
Qt/QML wrapper library for the ZXing bar-code image processing library.


%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%forgeautosetup -p1


%build
%qmake PREFIX=%{_prefix} INSTALL_LIBDIR=%{_libdir} src/ -o build/
%make_build -C build


%install
%make_install INSTALL_ROOT=%{buildroot} -C build


%files
%license LICENSE
%doc README.md
%{_libdir}/libQZXing.so.3
%{_libdir}/libQZXing.so.3.3
%{_libdir}/libQZXing.so.3.3.0


%files devel
%{_includedir}/QZXing.h
%{_includedir}/QZXing_global.h
%{_libdir}/libQZXing.so
%{_libdir}/pkgconfig/QZXing.pc


%changelog
%autochangelog
