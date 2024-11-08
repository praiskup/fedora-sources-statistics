# Generated by go2rpm 1.13.1
%bcond_without check
%global debug_package %{nil}

# https://github.com/akosmarton/papipes
%global goipath         github.com/akosmarton/papipes
%global commit          3c63b4919c769c9c2b2d07e69a98abb0eb47fe64

%gometa -L -f

%global common_description %{expand:
Pulseaudio client library in Golang for creating virtual sinks and sources.}

%global golicenses      LICENSE
%global godocs          example README.md

Name:           golang-github-akosmarton-papipes
Version:        0
Release:        %autorelease -p
Summary:        Pulseaudio library for creating virtual sinks and sources

License:        MIT
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

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
