%bcond_without check

# https://github.com/haproxytech/config-parser
%global debug_package %{nil}

%global goipath         github.com/haproxytech/config-parser
Version:                4.0.0~rc2
%global commit          12e472fc123e747c019d30f230cbb989df695354

%gometa

%global goaltipaths     %{goipath}/v4

%global common_description %{expand:
HAProxy configuration parser.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        HAProxy configuration parser

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/gofrs/flock)
BuildRequires:  golang(github.com/google/renameio)
BuildRequires:  golang(github.com/haproxytech/go-logger)

%description
%{common_description}

%gopkg

%prep
%goprep

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog
