%global realname poolboy

Name:		erlang-%{realname}
Version:	1.5.2
Release:	%autorelease
BuildArch:	noarch
Summary:	A hunky Erlang worker pool factory
License:	Unlicense OR ISC
URL:		https://github.com/devinus/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3

%description
%{summary}.

%prep
%setup -q -n %{realname}-%{version}
# FIXME plugins are currently broken
sed -i -e '/rebar3_eqc/d' rebar.config

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE UNLICENSE
%doc README.md
%{erlang_appdir}/

%changelog
%autochangelog
