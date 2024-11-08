%global realname jsx

Name:		erlang-%{realname}
Version:	3.1.0
Release:	%autorelease
BuildArch:	noarch
Summary:	A streaming, evented json parsing toolkit
License:	MIT
URL:		https://github.com/talentdeficit/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/v%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-jsx-0001-Adapt-to-OTP-24.patch
BuildRequires:	erlang-rebar3

%description
An Erlang application for consuming, producing and manipulating json. inspired
by yajl.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc CHANGES.md README.md
%{erlang_appdir}/

%changelog
%autochangelog
