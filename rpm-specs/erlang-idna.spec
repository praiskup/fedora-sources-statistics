%global srcname idna

Name:       erlang-%{srcname}
Version:    6.1.1
Release:    %autorelease
BuildArch:  noarch
License:    MIT
Summary:    A pure Erlang IDNA implementation that folllows RFC5891
URL:        https://github.com/benoitc/erlang-%{srcname}
VCS:        git:%{url}.git
Source0:    %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch1:     erlang-idna-0001-remove-unicode_util_compat-library.patch
BuildRequires: erlang-rebar3


%description
%{summary}.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license LICENSE
%doc CHANGELOG
%doc README.md
%{erlang_appdir}


%changelog
%autochangelog
