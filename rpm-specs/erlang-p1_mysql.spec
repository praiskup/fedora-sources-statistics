%global srcname p1_mysql


Name:       erlang-%{srcname}
Version:    1.0.25
Release:    %autorelease
BuildArch:  noarch
Summary:    Pure Erlang MySQL driver
License:    BSD-3-Clause
URL:        https://github.com/processone/%{srcname}
VCS:        git:%{url}.git
Source0:    %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch1:     erlang-p1_mysql-0001-Disable-Rebar3-plugins.patch
BuildRequires: erlang-rebar3


%description
This is an Erlang MySQL driver, used by ejabberd.


%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license COPYING
%doc README.md
%{erlang_appdir}


%changelog
%autochangelog
