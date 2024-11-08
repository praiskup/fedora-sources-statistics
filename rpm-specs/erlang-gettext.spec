%global realname gettext
%global git_commit 2bcba56069721afc7d8c58f84ce701958ec7a761
%global git_date 20170123


Name:		erlang-%{realname}
Version:	2.1.0
Release:	%autorelease -p -s %{git_date}git%{sub %git_commit 0 7}
BuildArch:	noarch
Summary:	Erlang internationalization library
License:	MIT
URL:		https://github.com/etnt/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{git_commit}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3


%description
%{summary}.


%prep
%autosetup -p1 -n %{realname}-%{git_commit}


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc README
%{erlang_appdir}/


%changelog
%autochangelog
