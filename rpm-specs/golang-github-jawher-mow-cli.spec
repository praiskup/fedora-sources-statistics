# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/jawher/mow.cli
%global goipath         github.com/jawher/mow.cli
Version:                1.2.0

%gometa

%global common_description %{expand:
Package Cli provides a framework to build command line applications in Go with
most of the burden of arguments parsing and validation placed on the framework
instead of the user.}

%global golicenses      LICENSE
%global godocs          README.md README.md.template

Name:           %{goname}
Release:        %autorelease
Summary:        Versatile library for building CLI applications in Go

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/assert)
BuildRequires:  golang(github.com/stretchr/testify/require)
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