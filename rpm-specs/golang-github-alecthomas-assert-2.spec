# Generated by go2rpm 1.8.2
%bcond_without check
%global debug_package %{nil}

# https://github.com/alecthomas/assert
%global goipath         github.com/alecthomas/assert/v2
Version:                2.10.0

%gometa -f

%global common_description %{expand:
A simple assertion library using Go generics.}

%global golicenses      COPYING
%global godocs          README.md bin/README.hermit.md

Name:           %{goname}
Release:        %autorelease
Summary:        A simple assertion library using Go generics

License:        MIT
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
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog