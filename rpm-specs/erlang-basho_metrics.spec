%global realname basho_metrics


Name:		erlang-%{realname}
Version:	1.0.0
Release:	%autorelease
Summary:	Fast performance metrics for Erlang
License:	Apache-2.0
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-basho_metrics-0001-Use-C-11.patch
BuildRequires:	boost-devel
BuildRequires:	erlang-rebar3
BuildRequires:	gcc-c++


%description
An open source Erlang library for efficient calculation of service performance
metrics.


%prep
%autosetup -p1 -n %{realname}-%{version}
rm -rf c_src/boost


%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p ./priv
g++ c_src/basho_metrics_nifs.cpp $CXXFLAGS -fPIC -std=c++11 -c -I%{_libdir}/erlang/usr/include -o c_src/basho_metrics_nifs.o
g++ c_src/basho_metrics_nifs.o $LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -lstdc++ -o priv/basho_metrics_nifs.so


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc README.org
%{erlang_appdir}/


%changelog
%autochangelog
