# Generated by go2rpm 1.9.0
# It needs network to dowload jquery map for testing
%bcond_with check
%global debug_package %{nil}

# https://github.com/go-sourcemap/sourcemap
%global goipath         gopkg.in/sourcemap.v1
%global forgeurl        https://github.com/go-sourcemap/sourcemap
Version:                1.0.5

%gometa

%global common_description %{expand:
Source maps consumer for Golang.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Source maps consumer for Golang

License:        BSD-2-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep
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