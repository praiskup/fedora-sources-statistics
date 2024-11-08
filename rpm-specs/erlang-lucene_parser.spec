%global realname lucene_parser
%global git_commit 7818ac9e7a4f1af60e8b9d84a6ad27552d530f4b

Name:		erlang-%{realname}
Version:	1
Release:	%autorelease
BuildArch:	noarch
Summary:	A library for Lucene-like query syntax parsing
License:	Apache-2.0
URL:		https://github.com/basho/riak_search
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{git_commit}/%{realname}-%{version}.tar.gz
Patch1:		erlang-lucene_parser-0001-Move-tests-to-the-canonical-directory.patch
BuildRequires:	erlang-rebar3

%description
%{summary}.

%prep
%autosetup -p3 -n riak_search-%{git_commit}/apps/%{realname}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%doc README.txt
%{erlang_appdir}/

%changelog
%autochangelog
