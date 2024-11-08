# Generated by go2rpm 1.8.2
# Fails on 32 bits arch
%ifnarch %{ix86} %{arm}
%bcond_without check
%endif
%global debug_package %{nil}

# https://github.com/aws/aws-sdk-go-v2
%global goipath         github.com/aws/aws-sdk-go-v2
Version:                20230724
%global tag             release-2023-07-24
%global distprefix      %{nil}

%gometa

%global common_description %{expand:
aws-sdk-go-v2 is the Developer Preview for the v2 of the AWS SDK for the Go
programming language.}

%global golicenses      LICENSE.txt NOTICE.txt
%global godocs          example CHANGELOG.md CODE_OF_CONDUCT.md\\\
                        CONTRIBUTING.md DESIGN.md README.md

Name:           %{goname}
Release:        %autorelease
Summary:        AWS SDK for the Go programming language

License:        Apache-2.0 AND BSD-3-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%install
%gopkginstall

%if %{with check}
%check
# aws/external: needs network
%gocheck -t aws/external -d aws/retry -t internal/repotools/changes -d service/internal/benchmark/dynamodb
%endif

%gopkgfiles

%changelog
%autochangelog
