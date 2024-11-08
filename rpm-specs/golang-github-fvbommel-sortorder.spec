# Generated by go2rpm 1.2
%bcond_without check

%global debug_package %{nil}

# https://github.com/fvbommel/sortorder
%global goipath         github.com/fvbommel/sortorder
Version:                1.1.0

%gometa

%global common_description %{expand:
Sort orders and comparison functions.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Sort orders and comparison functions

License:        MIT
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
