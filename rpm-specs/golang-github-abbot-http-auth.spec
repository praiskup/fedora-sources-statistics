# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/abbot/go-http-auth
%global goipath         github.com/abbot/go-http-auth
Version:                0.4.0
%global commit          860ed7f246ff5abfdbd5c7ce618fd37b49fd3d86

%gometa

# Remove in F33:
%global godevelheader %{expand:
Obsoletes:      golang-github-abbot-go-http-auth-devel < 0-0.20
}

%global common_description %{expand:
Basic and Digest HTTP Authentication for golang http.}

%global golicenses      LICENSE
%global godocs          examples README.md

%global gosupfiles      glide.lock glide.yaml

Name:           %{goname}
Release:        %autorelease
Summary:        Basic and Digest HTTP Authentication for golang http

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}
Source1:        glide.lock
Source2:        glide.yaml

BuildRequires:  golang(golang.org/x/crypto/bcrypt)
BuildRequires:  golang(golang.org/x/net/context)

%description
%{common_description}

%gopkg

%prep
%goprep
cp %{S:1} %{S:2} .

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog