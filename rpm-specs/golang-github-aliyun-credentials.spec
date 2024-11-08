%bcond_without check

# https://github.com/aliyun/credentials-go
%global debug_package %{nil}

%global goipath         github.com/aliyun/credentials-go
Version:                1.1.3

%gometa

%global common_description %{expand:
Alibaba Cloud (Aliyun) Credentials for Go.}

%global golicenses      LICENSE
%global godocs          CONTRIBUTING.md README-CN.md README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Alibaba Cloud (Aliyun) Credentials for Go

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/alibabacloud-go/debug/debug)
BuildRequires:  golang(github.com/alibabacloud-go/tea/tea)
BuildRequires:  golang(gopkg.in/ini.v1)

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/assert)
%endif

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
