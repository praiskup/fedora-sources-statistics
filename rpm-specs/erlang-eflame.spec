%global realname eflame
%global git_commit a08518142126f5fc541a3a3c4a04c27f24448bae
%global git_date 20150721


Name:		erlang-%{realname}
Version:	0
Release:	%autorelease -p -s %{git_date}git%{sub %git_commit 0 7}
BuildArch:	noarch
Summary:	Flame Graph profiler for Erlang
License:	MIT
URL:		https://github.com/slfritchie/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{git_commit}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3
BuildRequires:	perl-generators


%description
%{summary}.


%prep
%autosetup -p1 -n %{realname}-%{git_commit}


%build
%{erlang3_compile}


%install
%{erlang3_install}

install -D -p -m 0755 flamegraph.pl %{buildroot}%{erlang_appdir}/bin/flamegraph.pl
install -D -p -m 0755 flamegraph.riak-color.pl %{buildroot}%{erlang_appdir}/bin/flamegraph.riak-color.pl


%check
%{erlang3_test}


%files
%license LICENSE
%doc README.md README-Riak-Example.md
%{erlang_appdir}/


%changelog
%autochangelog
