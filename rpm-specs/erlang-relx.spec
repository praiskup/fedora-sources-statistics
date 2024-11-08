%global realname relx

Name:		erlang-%{realname}
Version:	4.10.0
Release:	%autorelease
BuildArch:	noarch
Summary:	Release assembler for Erlang/OTP Releases
License:	Apache-2.0
URL:		https://github.com/erlware/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/v%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-bbmustache
BuildRequires:	erlang-rebar3

%description
Relx assembles releases for an Erlang/OTP release. Given a release
specification and a list of directories in which to search for OTP applications
it will generate a release output.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE.md
%doc README.md
%{erlang_appdir}/

%changelog
%autochangelog
