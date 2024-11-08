%bcond_without check

# https://github.com/alibabacloud-go/tea
%global debug_package %{nil}

%global goipath         github.com/alibabacloud-go/tea
Version:                1.1.17

%gometa

%global common_description %{expand:
Alibaba Cloud (Aliyun) support for TEA OpenAPI DSL.}

%global golicenses      LICENSE
%global godocs          README-CN.md README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Alibaba Cloud (Aliyun) support for TEA OpenAPI DSL

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/alibabacloud-go/debug/debug)
BuildRequires:  golang(github.com/json-iterator/go)
BuildRequires:  golang(github.com/modern-go/reflect2)
BuildRequires:  golang(golang.org/x/net/proxy)

%description
%{common_description}

%gopkg

%prep
%goprep

%install
%gopkginstall

%if %{with check}
%check
%ifarch armv7hl i686
# Skip 'tea' tests due to 64-bit tests that will fail
%gocheck -d 'tea'
%else
%gocheck
%endif
%endif

%gopkgfiles

%changelog
%autochangelog
