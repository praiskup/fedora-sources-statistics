%global appname blurhash

Name: %{appname}-cpp
Version: 0.2.0
Release: %autorelease

License: BSL-1.0
Summary: C++ blurhash encoder/decoder
URL: https://github.com/Nheko-Reborn/%{appname}
Source0: %{url}/archive/v%{version}/%{appname}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: doctest-devel
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: meson

%description
Simple encoder and decoder for blurhashes. In large parts inspired by the
reference implementation.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{appname}-%{version} -p1
rm -f stb_*.h

%build
%meson -Dtests=true -Dwerror=false
%meson_build

%install
%meson_install

%check
%meson_test

%files
%doc README.md
%license LICENSE
%{_libdir}/lib%{appname}.so.0*

%files devel
%{_includedir}/%{appname}.hpp
%{_libdir}/lib%{appname}.so
%{_libdir}/pkgconfig/%{appname}.pc

%changelog
%autochangelog
