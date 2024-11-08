%global realname skerl


Name:		erlang-%{realname}
Version:	1.1.0
Release:	%autorelease
Summary:	Skein hash function for Erlang, via NIFs
# Original skein sources are in Public Domain
# src/hex.erl and src/skerl.erl are licensed under MIT
License:	LicenseRef-Fedora-Public-Domain and MIT
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-skerl-0001-Rewrote-hex-routines-under-MIT-license.patch
Patch2:		erlang-skerl-0002-Rewrote-Erlang-NIF-API-routines-under-MIT-license.patch
Patch3:		erlang-skerl-0003-Note-we-re-using-system-wide-header.patch
Patch4:		erlang-skerl-0004-Drop-R13B04-compatibility.patch
Patch5:		erlang-skerl-0005-Use-generic-endiannes-check-and-dron-IA-64-bits.patch
Patch6:		erlang-skerl-0006-Use-standard-headers.patch
Patch7:		erlang-skerl-0007-Fix-rebar-deprecation-warnings.patch
BuildRequires:	erlang-rebar3
BuildRequires:	gcc-c++


%description
Skein hash function for Erlang, via NIFs.


%prep
%autosetup -p1 -n %{realname}-%{version}


%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p priv
gcc c_src/skein.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/skein.o
gcc c_src/skein_api.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/skein_api.o
gcc c_src/skein_block.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/skein_block.o
gcc c_src/skerl_nifs.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/skerl_nifs.o
gcc c_src/skein.o c_src/skein_api.o c_src/skein_block.o c_src/skerl_nifs.o $LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -o priv/skerl_nifs.so


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%{erlang_appdir}/


%changelog
%autochangelog
