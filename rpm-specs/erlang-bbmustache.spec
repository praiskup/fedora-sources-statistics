%global realname bbmustache

Name:		erlang-%{realname}
Version:	1.12.2
Release:	%autorelease
BuildArch:	noarch
Summary:	Binary pattern match-based Mustache template engine for Erlang
License:	MIT
URL:		https://github.com/soranoba/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/v%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-bbmustache-0001-FIXME-Rebar3-plugins-are-currently-broken.patch
BuildRequires:	erlang-rebar3

%description
%{summary}.

%prep
%autosetup -p 1 -n %{realname}-%{version}
# FIXME this test requires escriptized bbmustache which we do not ship (yet?)
#rm -rf ct/bbmustache_escript_SUITE.erl ct/bbmustache_escript_SUITE_data/
# FIXME we cannot pass Common_Tests suite because of the missing deps. At least
# we can pass eunit ones.
rm -rf ct/*

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc doc/ README.md
%{erlang_appdir}/

%changelog
%autochangelog
