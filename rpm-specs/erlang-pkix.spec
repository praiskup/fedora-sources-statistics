%global srcname pkix

Name:       erlang-%{srcname}
Version:    1.0.10
Release:    %autorelease
BuildArch:  noarch
License:    Apache-2.0
Summary:    PKIX certificates management for Erlang
URL:        https://github.com/processone/%{srcname}
VCS:        git:%{url}.git
Source0:    %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildRequires: erlang-rebar3
Requires: ca-certificates


%description
A library for managing TLS certificates in Erlang.


%prep
%autosetup -p1 -n %{srcname}-%{version}
rm -rf ./rebar ./rebar.config ./rebar.config.script


%build
%{erlang3_compile}


%install
%{erlang3_install}

# pkix includes a CA bundle in priv/cacert.pem. Let's use a symlink to Fedora's CA bundle instead.
install -d -m 0755 %{buildroot}/%{erlang_appdir}/priv
ln -s /etc/pki/tls/certs/ca-bundle.trust.crt %{buildroot}/%{erlang_appdir}/priv/cacert.pem


%check
%{erlang3_test}


%files
%license LICENSE
%doc README.md
%{erlang_appdir}


%changelog
%autochangelog
