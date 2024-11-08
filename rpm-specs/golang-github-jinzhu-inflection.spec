# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/jinzhu/inflection
%global goipath         github.com/jinzhu/inflection
Version:                1.0.0

%gometa

%global common_description %{expand:
Inflection pluralizes and singularizes English nouns.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Pluralizes and singularizes English nouns

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
