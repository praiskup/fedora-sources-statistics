# Generated by go2rpm 1.6.0
# Fails on 32 bits arch
%ifnarch %{ix86} %{arm}
%bcond_without check
%endif
%global debug_package %{nil}

# https://github.com/aws/aws-sdk-go
%global goipath         github.com/aws/aws-sdk-go
Version:                1.44.307

%gometa

%global common_description %{expand:
Aws-sdk-go is the official AWS SDK for the Go programming language.}

%global golicenses      LICENSE.txt NOTICE.txt
%global godocs          example CHANGELOG_PENDING.md CODE_OF_CONDUCT.md CONTRIBUTING.md README.md CHANGELOG.MIGRATION_GUIDE

Name:           %{goname}
Release:        %autorelease
Summary:        AWS SDK for the Go programming language

License:        BSD-3-Clause AND Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%install
%gopkginstall

%if %{with check}
%check
%gocheck -d aws/session
%endif

%gopkgfiles

%changelog
%autochangelog