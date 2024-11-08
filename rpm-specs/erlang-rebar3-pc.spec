%global realname pc


Name:		erlang-rebar3-%{realname}
Version:	1.15.0
Release:	%autorelease
Summary:	A port compiler for rebar3
License:	MIT
URL:		https://github.com/blt/port_compiler
VCS:		git:%{url}.git
Source0:	%{url}/archive/v%{version}/port_compiler-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	erlang-rebar3
# Required for port compiling but cannot be picked up automatically yet
Requires:	erlang-erl_interface


%description
This plugin is intended to replicate the rebar2 support for compiling native
code. It is not a drop-in replacement in terms of command-line interface but
the exact configuration interface in projects' rebar.configs have been
preserved.


%prep
%autosetup -p1 -n port_compiler-%{version}


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
