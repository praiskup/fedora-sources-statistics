# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/daviddengcn/go-assert
%global goipath         github.com/daviddengcn/go-assert
%global commit          ba7e68aeeff6e81e6a7699c9e603d342e4b2b919

%gometa

%global common_description %{expand:
Testing utils for Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Testing utils for Go

# Upstream license specification: BSD-3-Clause
License:        BSD-3-Clause
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/daviddengcn/go-algs/ed)
BuildRequires:  golang(github.com/daviddengcn/go-villa)

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