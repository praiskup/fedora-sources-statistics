%global realname webmachine

Name:		erlang-%{realname}
Version:	1.11.1
Release:	%autorelease
BuildArch:	noarch
Summary:	A REST-based system for building web applications
License:	Apache-2.0
URL:		https://github.com/webmachine/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-webmachine-0001-Disable-faulty-test.patch
Patch2:		erlang-webmachine-0002-Enable-verbose-output-during-testing.patch
Patch3:		erlang-webmachine-0003-webmachine_util-fix-handling-of-0.0-for-OTP-26.1-27..patch
Patch4:		erlang-webmachine-0004-add-a-pre-extension-file-name-to-make-guess_mime_tes.patch
Patch5:		erlang-webmachine-0005-Create-CI-github-actions-workflow.patch
Patch6:		erlang-webmachine-0006-FIXME-this-test-fails-constantly.patch
BuildRequires:	erlang-ibrowse
BuildRequires:	erlang-meck
BuildRequires:	erlang-mochiweb
BuildRequires:	erlang-rebar3

%description
%{summary}.

%prep
%autosetup -p1 -n %{realname}-%{version}
chmod 644 src/wmtrace_resource.erl
chmod -x priv/trace/wmtrace.css
chmod -x priv/trace/wmtrace.js

%build
%{erlang3_compile}

%install
%{erlang3_install}
# Additional resources
cp -arv priv %{buildroot}%{erlang_appdir}/

%check
%{erlang3_test}

%files
%license LICENSE
%doc docs/http-headers-status-v3.png README.md THANKS
%{erlang_appdir}/

%changelog
%autochangelog
