# Generated by go2rpm 1.14.0
# gitleak's fork of gitdiff has some changes that break tests.
# Notified developer as project doesn't accept issues, waiting feedback.
%bcond check 0
%bcond bootstrap 0

%global debug_package %{nil}
%if %{with bootstrap}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(.*\\)$
%endif

# https://github.com/gitleaks/go-gitdiff
%global goipath         github.com/gitleaks/go-gitdiff
Version:                0.9.1

%gometa -L -f

%global common_description %{expand:
Go library for parsing and applying patches created by Git.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           golang-github-gitleaks-gitdiff
Release:        %autorelease
Summary:        Go library for parsing and applying patches created by Git

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