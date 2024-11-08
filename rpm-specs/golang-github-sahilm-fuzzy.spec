# Generated by go2rpm 1.10.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/sahilm/fuzzy
%global goipath         github.com/sahilm/fuzzy
Version:                0.1.1

%gometa -L -f

%global common_description %{expand:
Go library that provides fuzzy string matching optimized for filenames and code
symbols in the style of Sublime Text, VSCode, IntelliJ IDEA et al.}

%global golicenses      LICENSE
%global godocs          _example CONTRIBUTING.md README.md

Name:           golang-github-sahilm-fuzzy
Release:        %autorelease
Summary:        Go library that provides fuzzy string matching

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
