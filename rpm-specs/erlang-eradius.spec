%global realname eradius

Name:		erlang-%{realname}
Version:	2.3.1
Release:	%autorelease
BuildArch:	noarch
Summary:	Erlang RADIUS server framework
License:	MIT
URL:		https://github.com/travelping/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-eradius-0001-Ignore-plugins.patch
Patch2:		erlang-eradius-0002-Disable-prometheus-support.patch
BuildRequires:	erlang-meck
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
%doc METRICS.md README.md sample/
%{erlang_appdir}/

%changelog
%autochangelog
