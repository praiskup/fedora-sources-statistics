%global realname exometer_core

Name:		erlang-%{realname}
Version:	1.7.1
Release:	%autorelease
BuildArch:	noarch
Summary:	Easy and efficient instrumentation of Erlang code
License:	MPL-2.0
URL:		https://github.com/feuerlabs/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-exometer_core-0001-FIXME-disable-plugins-for-Rebar3.patch
BuildRequires:	erlang-edown
BuildRequires:	erlang-hut
BuildRequires:	erlang-meck
BuildRequires:	erlang-parse_trans
BuildRequires:	erlang-rebar3
BuildRequires:	erlang-setup

%description
The Exometer Core package allows for easy and efficient instrumentation of
Erlang code, allowing crucial data on system performance to be exported to a
wide variety of monitoring systems.

Exometer Core comes with a set of predefined monitor components, and can be
expanded with custom components to handle new types of Metrics, as well as
integration with additional external systems such as databases, load balancers,
etc.

%prep
%autosetup -p1 -n %{realname}-%{version}
# FIXME don't generate docs for now
rm -f doc/overview.edoc

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc doc/ README.md
%{erlang_appdir}/

%changelog
%autochangelog
