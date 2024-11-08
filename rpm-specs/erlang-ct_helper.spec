%global realname ct_helper
%global git_commit 395618eb84cada02875670aec6c3e8f9d923b1f8
%global git_date 20240118


Name:		erlang-%{realname}
Version:	0
Release:	%autorelease -p -s %{git_date}git%{sub %git_commit 0 7}
BuildArch:	noarch
Summary:	Helper modules for common_test suites
License:	ISC
URL:		https://github.com/ninenines/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{git_commit}/%{realname}-%{version}.tar.gz
BuildRequires:  erlang-rebar3


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
%doc README.md
%{erlang_appdir}/


%changelog
%autochangelog
