%global realname riakc


Name:		erlang-riak_client
Version:	2.5.3
Release:	%autorelease
BuildArch:	noarch
Summary:	Erlang client for Riak
License:	Apache-2.0
URL:		https://github.com/basho/riak-erlang-client
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/riak_client-%{version}.tar.gz
Patch1:		erlang-riak_client-0001-Allow-more-Erlang-versions.patch
Patch2:		erlang-riak_client-0002-Add-deprecation-for-Erlang-20-as-well.patch
Patch3:		erlang-riak_client-0003-Remove-excessive-export_all-directive.patch
BuildRequires:	erlang-rebar3
BuildRequires:	erlang-riak_pb


%description
Erlang client for Riak.


%prep
%autosetup -p1 -n riak-erlang-client-%{version}


%build
%{erlang3_compile}
rebar3 edoc -vv
rm -f edoc/edoc-info


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc README.md edoc/
%{erlang_appdir}/


%changelog
%autochangelog
