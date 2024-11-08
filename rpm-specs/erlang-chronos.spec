%global realname chronos

Name:		erlang-%{realname}
Version:	0.5.1
Release:	%autorelease
BuildArch:	noarch
Summary:	Timer utility for Erlang tests
License:	MIT
URL:		https://github.com/lehoff/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3

%description
%{summary}.

%prep
%autosetup -p1 -n %{realname}-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
# Requires a proprietary eqc library
#%%{erlang3_test}

%files
%doc
%{erlang_appdir}/

%changelog
%autochangelog
