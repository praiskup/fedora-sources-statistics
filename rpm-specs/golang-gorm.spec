# Generated by go2rpm 1.3
%bcond_without check

%global debug_package %{nil}

# https://github.com/go-gorm/gorm
%global goipath         gorm.io/gorm
%global forgeurl        https://github.com/go-gorm/gorm
Version:                1.20.11

%gometa

%global common_description %{expand:
The fantastic ORM library for Golang, aims to be developer friendly.}

%global golicenses      License
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        ORM library for Golang

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/jinzhu/inflection)
BuildRequires:  golang(github.com/jinzhu/now)

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