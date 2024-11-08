%bcond_without check

# https://github.com/labbsr0x/bindman-dns-webhook
%global debug_package %{nil}

%global goipath         github.com/labbsr0x/bindman-dns-webhook
Version:                1.0.2

%gometa

%global common_description %{expand:
Go library to define the webhook needed by a Bindman DNS Manager in order to
ease out integrations among clients and managers.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Go library for Bindman DNS Manager
License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/go-errors/errors)
BuildRequires:  golang(github.com/gorilla/mux)
BuildRequires:  golang(github.com/labbsr0x/goh/gohclient)
BuildRequires:  golang(github.com/prometheus/client_golang/prometheus)
BuildRequires:  golang(github.com/prometheus/client_golang/prometheus/promhttp)
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
