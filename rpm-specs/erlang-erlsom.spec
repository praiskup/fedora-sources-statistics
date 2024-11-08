%global realname erlsom


Name:		erlang-%{realname}
Version:	1.5.1
Release:	%autorelease
BuildArch:	noarch
Summary:	Support for XML Schema in Erlang
License:	LGPL-3.0-or-later
URL:		https://github.com/willemdj/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/v%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar3


%description
Erlsom is a set of functions to deal with XML Schema (XSDs) in Erlang.
First you 'compile' the schema, and after that you can parse XML
documents that conform to the schema. The result is a structure of
Erlang records, based on the types that are defined by the Schema.
Or, the other way around, a structure of records can be translated
to an XML document.


%prep
%autosetup -p1 -n %{realname}-%{version}


%build
%{erlang3_compile}


%install
%{erlang3_install}


%check
%{erlang3_test}


%files
%license COPYING COPYING.LESSER
%doc examples/ doc/ README.md
%{erlang_appdir}/


%changelog
%autochangelog
