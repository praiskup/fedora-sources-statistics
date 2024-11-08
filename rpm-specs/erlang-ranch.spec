%global realname ranch
%global git_commit a8f31f3f0274f7e5a6b58fa6b6090c3160c4d023
%global git_date 20240108


Name:		erlang-%{realname}
Version:	2.1.0
Release:	%autorelease -s %{git_date}git%{sub %git_commit 0 7}
BuildArch:	noarch
Summary:	Socket acceptor pool for TCP protocols
License:	ISC
URL:		https://github.com/ninenines/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{git_commit}/%{realname}-%{git_commit}.tar.gz
Patch1:		erlang-ranch-0001-Fix-testing-with-rebar.patch
Patch2:		erlang-ranch-0002-Don-t-care-about-return-value.patch
BuildRequires:	erlang-ct_helper
BuildRequires:	erlang-rebar3


%description
%{summary}.


%prep
%autosetup -p1 -n %{realname}-%{git_commit}
# FIXME we don't have stampede yet
rm -f test/stampede_SUITE.erl
# FIXME this test is very fragile and cannot be run with Rebar3 directly
rm -f test/upgrade_SUITE.erl


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc README.asciidoc doc/ examples/
%{erlang_appdir}/


%changelog
%autochangelog
