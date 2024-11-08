%bcond_without check

# https://github.com/alyu/configparser
%global debug_package %{nil}

%global goipath         github.com/alyu/configparser
%global commit          744e9a66e7bcb83ea09084b979ddd1efc1f2f418

%gometa

%global common_description %{expand:
Alibaba Cloud (Aliyun) INI configuration file parser for Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Alibaba Cloud (Aliyun) INI configuration file parser for Go

# Upstream license specification: BSD-3-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            %{gourl}
Source0:        %{gosource}

%if %{with check}
# Tests
BuildRequires:  perl-Digest-SHA
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
