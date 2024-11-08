%global srcname cache_tab
%global p1_utils_ver 1.0.26

Name: erlang-%{srcname}
Version: 1.0.31
Release: %autorelease
License: Apache-2.0
Summary: Erlang cache table application
URL: https://github.com/processone/%{srcname}
VCS: git:%{url}.git
Source0: %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch1: erlang-cache_tab-0001-FIXME-Rebar3-plugins-are-broken.patch
BuildRequires: gcc
BuildRequires: erlang-rebar3
BuildRequires: erlang-p1_utils >= %{p1_utils_ver}
Requires: erlang-p1_utils >= %{p1_utils_ver}


%description
This application is intended to proxy back-end operations for Key-Value insert,
lookup and delete and maintain a cache of those Key-Values in-memory, to save
back-end operations. Operations are intended to be atomic between back-end and
cache tables. The lifetime of the cache object and the max size of the cache
can be defined as table parameters to limit the size of the in-memory tables.


%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p ./priv/lib
gcc c_src/ets_cache.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/ets_cache.o
gcc c_src/ets_cache.o $LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -ldl -o priv/lib/ets_cache.so


%install
%{erlang3_install}

install -p -D -m 755 priv/lib/* --target-directory=%{buildroot}%{erlang_appdir}/priv/lib/


%check
%{erlang3_test}


%files
%license LICENSE.txt
%doc CHANGELOG.md
%doc README.md
%{erlang_appdir}/


%changelog
%autochangelog
