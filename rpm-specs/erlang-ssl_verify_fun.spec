%global realname ssl_verify_fun

Name:     erlang-%{realname}
Version:  1.1.6
Release:  %autorelease
Summary:  Collection of ssl verification functions for Erlang
License:  MIT
URL:      https://github.com/deadtrickster/%{realname}.erl
VCS:      git:%{url}.git
Source0:  %{url}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  erlang-rebar3

%description
%{summary}.

%prep
%autosetup -p1 -n %{realname}.erl-%{version}

%build
%{erlang3_compile}

%install
%{erlang3_install}

%check
%{erlang3_test}

%files
%license LICENSE
%doc README.md
%{erlang_appdir}/

%changelog
%autochangelog
