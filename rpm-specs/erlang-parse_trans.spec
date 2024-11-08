%global realname parse_trans


Name:		erlang-%{realname}
Version:	3.4.1
Release:	%autorelease
BuildArch:	noarch
Summary:	Parse transform utilities for Erlang
License:	Apache-2.0
URL:		https://github.com/uwiger/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-edown
BuildRequires:	erlang-rebar3


%description
%{summary}.


%prep
%autosetup -p 1 -n %{realname}-%{version}


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc doc/ examples/ README.md
%{erlang_appdir}/


%changelog
%autochangelog
