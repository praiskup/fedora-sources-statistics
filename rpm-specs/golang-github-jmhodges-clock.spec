# Generated by go2rpm 1.6.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/jmhodges/clock
%global goipath         github.com/jmhodges/clock
Version:                1.2.0

%gometa

%global common_description %{expand:
Package clock provides an abstraction for system time that enables testing of
time-sensitive code.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Abstraction for system time that enables testing of time-sensitive code

License:        MIT
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
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog