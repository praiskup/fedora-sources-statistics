%global realname merge_index


Name:		erlang-%{realname}
Version:	2.1
Release:	%autorelease
BuildArch:	noarch
Summary:	An Erlang library for storing ordered sets on disk
License:	Apache-2.0
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-merge_index-0001-erlang-get_stacktrace-was-deprecated-long-time-ago.patch
BuildRequires:	erlang-lager
BuildRequires:	erlang-rebar3


%description
MergeIndex is an Erlang library for storing ordered sets on disk. It is very
similar to an SSTable (in Google's Bigtable) or an HFile (in Hadoop).


%prep
%autosetup -p1 -n %{realname}-%{version}


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
# Requires quickcheck which is proprietary software
# w/o it it just returns ok
%{erlang3_test}


%files
%license LICENSE
%doc Notes.txt README.md
%{erlang_appdir}/


%changelog
%autochangelog
