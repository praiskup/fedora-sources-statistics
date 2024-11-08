%global realname erlsyslog

Name:		erlang-%{realname}
Version:	0.8.0
Release:	%autorelease
Summary:	Syslog facility for Erlang
License:	MIT
URL:		https://github.com/lemenkov/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3
BuildRequires:	gcc

%description
%{summary}.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
mkdir -p ./ebin
sed -i -e "s,%VSN%,%{version},g" src/erlsyslog.app.src > ebin/erlsyslog.app

%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p priv/
gcc c_src/erlsyslog_drv.c	$CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/erlsyslog_drv.o
gcc c_src/erlsyslog_drv.o	$LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -o priv/erlsyslog_drv.so

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%doc example
%{erlang_appdir}/

%changelog
%autochangelog
