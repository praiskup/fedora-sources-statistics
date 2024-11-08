%global realname mozjs


Name:		erlang-js
Version:	1.9.3
Release:	%autorelease
Summary:	A Friendly Erlang to Javascript Binding
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:	Apache-2.0
URL:		http://github.com/erlang-mozjs/erlang-%{realname}
VCS:		scm:git:%{url}.git
Source0:	%{url}/archive/%{version}/erlang-%{realname}-%{version}.tar.gz
# https://github.com/erlang-mozjs/erlang-mozjs/pull/8
Patch01:    0001-Switch-default-mozjs-to-mozjs102.patch

BuildRequires:	erlang-mochiweb
BuildRequires:	erlang-rebar
BuildRequires:	gcc-c++
BuildRequires:	mozjs102-devel


%description
A Friendly Erlang to Javascript Binding.


%prep
%autosetup -p1 -n erlang-%{realname}-%{version}


%build
%{erlang_compile}


%install
%{erlang_install}
install -m 644 priv/json2.js $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%check
# FIXME FIXME FIXME
# Fails with "too much recursion" on s390x, and I don't have access to any s390x machines
# Tracking bug - https://github.com/erlang-mozjs/erlang-mozjs/issues/1
# FIXME FIXME FIXME also strange issues on armv7hl, aarch64 (on armv7hl also
# but nobody cares anymore)
%ifnarch s390x aarch64
%{erlang_test}
%endif


%files
%license LICENSE
%doc README.org
%{erlang_appdir}/


%changelog
%autochangelog
