%global realname goldrush

Name:		erlang-%{realname}
Version:	0.2.0
Release:	%autorelease
BuildArch:	noarch
Summary:	Small, fast event processing and monitoring for Erlang/OTP applications
License:	MIT
URL:		https://github.com/DeadZen/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3

%description
A small Erlang app that provides fast event stream processing.

%prep
%autosetup -n %{realname}-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc README.org
%{erlang_appdir}/

%changelog
%autochangelog
