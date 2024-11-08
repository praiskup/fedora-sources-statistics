%global realname riak_sysmon

Name:		erlang-%{realname}
Version:	2.2.1
Release:	%autorelease
BuildArch:	noarch
Summary:	Rate-limiting system_monitor event handler for Riak
License:	Apache-2.0
URL:		https://github.com/basho/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-riak_sysmon-0001-Move-test-handled-to-test-directory.patch
Patch2:		erlang-riak_sysmon-0002-Remove-example-handler.patch
BuildRequires:	erlang-cuttlefish
BuildRequires:	erlang-rebar3

%description
Simple OTP app for managing Erlang VM system_monitor event messages.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}
cp -arv priv/ %{buildroot}%{erlang_appdir}/

%check
%{erlang3_test}

%files
%license LICENSE
%doc doc/ example/ README.md
%{erlang_appdir}/

%changelog
%autochangelog
