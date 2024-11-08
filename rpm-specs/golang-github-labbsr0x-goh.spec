%bcond_without check

# https://github.com/labbsr0x/goh
%global debug_package %{nil}

%global goipath         github.com/labbsr0x/goh
Version:                1.0.1

%gometa

%global common_description %{expand:
Utility lib for writing extremely simple webhooks in go, among other things.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Go library for writing simple webhooks
License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/go-cmd/cmd)
BuildRequires:  golang(github.com/go-errors/errors)
BuildRequires:  golang(github.com/sirupsen/logrus)

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
