# Generated by go2rpm
# There are some precision problems with some architectures
# https://github.com/montanaflynn/stats/issues/33
%global debug_package %{nil}

# For now, We are skipping the failing tests
%bcond_with check

# https://github.com/montanaflynn/stats
%global goipath         github.com/montanaflynn/stats
Version:                0.6.6

%gometa

%global common_description %{expand:
A well tested and comprehensive Golang statistics library package with no
dependencies.}

%global golicenses      LICENSE
%global godocs          examples CHANGELOG.md README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Well tested and comprehensive Golang statistics library package

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