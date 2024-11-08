%global realname sd_notify


Name:		erlang-%{realname}
Version:	1.1
Release:	%autorelease
BuildArch:	noarch
Summary:	Erlang interface to systemd notify subsystem
License:	MIT
URL:		https://github.com/systemd/erlang-%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/v%{version}/erlang-%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3


%description
%{summary}.


%prep
%autosetup


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%{erlang_appdir}/


%changelog
%autochangelog
