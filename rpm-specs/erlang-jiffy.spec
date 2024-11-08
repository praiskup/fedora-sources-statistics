%global realname jiffy


Name:           erlang-%{realname}
Version:        1.1.2
Release:        %autorelease
Summary:        Erlang JSON parser
# Automatically converted from old format: MIT and BSD - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND LicenseRef-Callaway-BSD
URL:            https://github.com/davisp/%{realname}
VCS:            git:%{url}.git
Source0:        %{url}/archive/%{version}/%{realname}-%{version}.tar.gz
# Use double conversion from the system instead of the bundled one
Patch1:         erlang-jiffy-0001-Use-double-conversion-from-the-system.patch
Patch2:		erlang-jiffy-0002-FIXME-Rebar3-plugins-currently-broken.patch
BuildRequires:  double-conversion-devel
BuildRequires:  erlang-rebar3
BuildRequires:  gcc-c++
Provides:       %{realname} = %{version}
Obsoletes:      %{realname} < %{version}


%description
A JSON parser for Erlang implemented as a NIF.


%prep
%autosetup -p 1 -n %{realname}-%{version}
# Use double conversion from the system instead of the bundled one
rm -r c_src/double-conversion
rm -rf rebar.config rebar.config.script


%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p priv/lib
g++ c_src/doubles.cc $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/doubles.o
g++ c_src/objects.cc $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/objects.o
gcc c_src/decoder.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/decoder.o
gcc c_src/encoder.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/encoder.o
gcc c_src/jiffy.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/jiffy.o
gcc c_src/termstack.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/termstack.o
gcc c_src/utf8.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/utf8.o
gcc c_src/util.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/util.o
g++ c_src/decoder.o c_src/encoder.o c_src/jiffy.o c_src/termstack.o c_src/utf8.o c_src/util.o c_src/doubles.o c_src/objects.o $LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -L%{_libdir} -lstdc++ -ldouble-conversion -o priv/jiffy.so

%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%doc README.md
%license LICENSE
%{erlang_appdir}/


%changelog
%autochangelog
