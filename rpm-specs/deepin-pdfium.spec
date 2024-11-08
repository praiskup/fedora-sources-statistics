Name:           deepin-pdfium
Version:        1.0.2
Release:        %autorelease
Summary:        development library for pdf on Deepin
# the library is under LGPL-3.0-or-later license
# pdfium: Apache-2.0
License:        LGPL-3.0-or-later AND Apache-2.0
URL:            https://github.com/linuxdeepin/deepin-pdfium
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make

BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  pkgconfig(chardet)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  libjpeg-turbo-devel

Provides:       bundled(pdfium)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1

%build
%qmake_qt5 LIB_INSTALL_DIR=%{_libdir}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE
%doc README.md
%{_libdir}/libdeepin-pdfium.so.1*

%files devel
%{_includedir}/deepin-pdfium/
%{_libdir}/libdeepin-pdfium.so
%{_libdir}/pkgconfig/deepin-pdfium.pc

%changelog
%autochangelog
