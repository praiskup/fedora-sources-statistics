# Generated by go2rpm 1.14.0
%bcond check 0
%bcond bootstrap 0

%global debug_package %{nil}
%if %{with bootstrap}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(.*\\)$
%endif

# https://github.com/alexflint/go-arg
%global goipath         github.com/alexflint/go-arg
Version:                1.5.1

%gometa -L -f

%global common_description %{expand:
Struct-based argument parsing in Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           golang-github-alexflint-arg
Release:        %autorelease
Summary:        Struct-based argument parsing in Go

License:        BSD-2-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

%if %{without bootstrap}
%generate_buildrequires
%go_generate_buildrequires
%endif

%install
%gopkginstall

%if %{without bootstrap}
%if %{with check}
%check
%gocheck
%endif
%endif

%gopkgfiles

%changelog
%autochangelog