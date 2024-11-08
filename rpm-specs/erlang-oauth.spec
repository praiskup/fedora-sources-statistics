%global realname oauth

Name:		erlang-%{realname}
Version:	2.1.0
Release:	%autorelease
BuildArch:	noarch
Summary:	An Erlang OAuth 1.0 implementation
License:	MIT
URL:		http://github.com/erlangpack/%{name}
VCS:		git:%{url}.git
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	erlang-rebar3

%description
An Erlang OAuth 1.0 implementation. Includes functions for generating
signatures (client side), verifying signatures (server side), and some
convenience functions for making OAuth HTTP requests (client side).

%prep
%setup -q

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%doc CHANGELOG.md README.md THANKS.txt
%license LICENSE.txt
%{erlang_appdir}/

%changelog
%autochangelog
