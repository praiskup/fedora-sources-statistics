%global realname hex_core

Name:     erlang-%{realname}
Version:  0.10.3
Release:  %autorelease
Summary:  Reference implementation of Hex specifications
License:  Apache-2.0
URL:      https://github.com/hexpm/%{realname}
VCS:      git:%{url}.git
Source0:  %{url}/archive/v%{version}/%{realname}-%{version}.tar.gz
Patch1:   erlang-hex_core-0001-FIXME-Rebar3-plugins-currently-broken.patch
Patch2:   erlang-hex_core-0002-FIXME-disable-faulty-tests.patch
BuildArch:     noarch
BuildRequires: erlang-proper
BuildRequires: erlang-rebar3

%description
%{summary}.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
{%erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc README.md examples/
%{erlang_appdir}/

%changelog
%autochangelog
