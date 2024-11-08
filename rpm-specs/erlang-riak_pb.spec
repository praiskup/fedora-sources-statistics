%global realname riak_pb
%global upstream basho


Name:		erlang-%{realname}
Version:	2.3.2
Release:	%autorelease
BuildArch:	noarch
Summary:	Riak Protocol Buffers Messages
License:	Apache-2.0
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-riak_pb-0001-Remove-export_all-directive.patch
# FIXME add Python and Java bindings
BuildRequires:	erlang-hamcrest
BuildRequires:	erlang-protobuffs >= 0.7.0
BuildRequires:	erlang-rebar3


%description
The message definitions for the Protocol Buffers-based interface to Riak and
various Erlang-specific utility modules for the message types.


%prep
%autosetup -p1 -n %{realname}-%{version}


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc README.md
%{erlang_appdir}/


%changelog
%autochangelog
