# Generated by go2rpm 1.14.0
%bcond check 1
%bcond bootstrap 0

%global debug_package %{nil}
%if %{with bootstrap}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(.*\\)$
%endif

# https://github.com/benbjohnson/clock
%global goipath         github.com/benbjohnson/clock
# WARNING: Latest version 1.3.5 breaks golang-uber-ratelimit
#          and upstream is archived.
Version:                1.3.0

%gometa -L

%global common_description %{expand:
Clock is a small library for mocking time in Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           golang-github-benbjohnson-clock
Release:        %autorelease
Summary:        Clock is a small library for mocking time in Go

License:        MIT
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