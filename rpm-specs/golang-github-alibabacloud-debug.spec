%bcond_without check

# https://github.com/alibabacloud-go/debug
%global debug_package %{nil}

%global goipath         github.com/alibabacloud-go/debug
%global commit          9472017b5c6804c66e5d873fabd2a2a937b31e0b

%gometa

%global common_description %{expand:
Alibaba Cloud (Aliyun) Debug function for Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Alibaba Cloud (Aliyun) Debug function for Go

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

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
