Name:           unibilium
Version:        2.1.2
Release:        %autorelease
Summary:        Terminfo parsing library

License:        LGPL-3.0-or-later
URL:            https://github.com/neovim/unibilium

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libtool
# For docs
BuildRequires:  %{_bindir}/pod2man
# For tests
BuildRequires:  %{_bindir}/prove

%description
Unibilium is a very basic terminfo library. It doesn't depend on curses or any
other library. It also doesn't use global variables, so it should be
thread-safe.

%package devel
Summary:        Development files needed for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1
autoreconf -fi

%build
%configure
%make_build

%install
%make_install
rm -vf %{buildroot}%{_libdir}/*.{a,la}

%check
make test

%ldconfig_scriptlets

%files
%license LGPLv3
%doc Changes
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}.h
%{_mandir}/man3/unibi_*.3*
%{_mandir}/man3/%{name}.h.3*

%changelog
%autochangelog
