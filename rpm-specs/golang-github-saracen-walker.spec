# Generated by go2rpm 1.3
%bcond_without check

%global debug_package %{nil}

# https://github.com/saracen/walker
%global goipath         github.com/saracen/walker
Version:                0.1.4

%gometa

%global common_description %{expand:
Walker is a faster, parallel version, of filepath.Walk.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Walker is a faster, parallel version, of filepath.Walk

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(golang.org/x/sync/errgroup)

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
