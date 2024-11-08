%global srcname p1_oauth2


Name:       erlang-%{srcname}
Version:    0.6.14
Release:    %autorelease
BuildArch:  noarch
License:    MIT
Summary:    An Oauth2 implementation for Erlang
URL:        https://github.com/processone/%{srcname}
VCS:        git:%{url}.git
Source0:    %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch1:     erlang-p1_oauth2-0001-FIXME-Rebar3-plugins-are-broken-right-now.patch
BuildRequires: erlang-meck >= 0.8.3
BuildRequires: erlang-proper
BuildRequires: erlang-rebar3


%description
This library is designed to simplify the implementation of the server side of
OAuth2. It is a fork of erlang-oauth2 by processone, and is needed by ejabberd.


%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%{erlang3_compile}


%check
%{erlang3_test}


%install
%{erlang3_install}


%files
%license LICENSE
%doc README.md
%{erlang_appdir}


%changelog
%autochangelog
