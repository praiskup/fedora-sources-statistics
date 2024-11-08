%global realname neotoma

Name:		erlang-%{realname}
Version:	1.7.4
Release:	%autorelease
BuildArch:	noarch
Summary:	Erlang library and packrat parser-generator for parsing expression grammars
License:	MIT
URL:		https://github.com/seancribbs/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3

%description
%{summary}.

%prep
%autosetup -p1 -n %{realname}-%{version}
# FIXME plugins are currently broken
sed -i -e '/rebar3_hex/d' rebar.config

%build
%{erlang3_compile}

%install
%{erlang3_install}
mkdir -p %{buildroot}%{erlang_appdir}/priv
install -p -m 0644 priv/neotoma_parse.peg priv/peg_includes.hrl %{buildroot}%{erlang_appdir}/priv/

%check
%{erlang3_test}

%files
%license LICENSE
%doc extra/ README.textile
%{erlang_appdir}/

%changelog
%autochangelog
