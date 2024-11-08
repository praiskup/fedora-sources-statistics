%global srcname iconv
%global p1_utils_ver 1.0.19

Name:       erlang-%{srcname}
Version:    1.0.13
Release:    %autorelease
Summary:    Fast encoding conversion library for Erlang / Elixir
License:    Apache-2.0
URL:        https://github.com/processone/%{srcname}
VCS:        scm:git:%{url}.git
Source0:    %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch1:     erlang-iconv-0001-Disable-port-compiler-until-we-package-it.patch
Provides:   erlang-p1_iconv = %{version}-%{release}
Obsoletes:  erlang-p1_iconv <= 1.0.0-2
BuildRequires: gcc
BuildRequires: erlang-p1_utils >= %{p1_utils_ver}
BuildRequires: erlang-rebar3
Requires: erlang-p1_utils >= %{p1_utils_ver}


%description
Erlang bindings for libiconv. This is used by ejabberd.


%prep
%autosetup -n %{srcname}-%{version}


%build
%configure --enable-nif
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p priv/lib
gcc c_src/iconv.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/iconv.o
gcc c_src/iconv.o $LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -o priv/lib/iconv.so


%install
%{erlang3_install}

install -d $RPM_BUILD_ROOT%{_erllibdir}/%{srcname}-%{version}/priv/lib
install -pm755 priv/lib/iconv.so $RPM_BUILD_ROOT%{_erllibdir}/%{srcname}-%{version}/priv/lib/


%check
%{erlang3_test}


%files
%license LICENSE.txt
%doc README.md
%{erlang_appdir}


%changelog
%autochangelog
