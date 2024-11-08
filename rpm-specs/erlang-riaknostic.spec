%global realname riaknostic

Name:		erlang-%{realname}
Version:	3.0.10
Release:	%autorelease
BuildArch:	noarch
Summary:	A diagnostic tool for Riak installations
License:	Apache-2.0
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/riak_kv-%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-lager
BuildRequires:	erlang-meck
BuildRequires:	erlang-rebar3

%description
A set of tools that diagnoses common problems which could affect a Riak node or
cluster. When experiencing any problem with Riak, riaknostic should be the
first thing run during troubleshooting. The tool is a plugin for Riak which can
be used via the riak-admin script.

%prep
%autosetup -p1 -n %{realname}-riak_kv-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}
cp -arv priv/ %{buildroot}%{erlang_appdir}/

%check
%{erlang3_test}

%files
%license LICENSE
%doc README.md doc/erlang.png doc/*.html doc/stylesheet.css
%{erlang_appdir}/

%changelog
%autochangelog
