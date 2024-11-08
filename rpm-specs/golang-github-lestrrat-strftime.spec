%bcond_without check

# https://github.com/lestrrat-go/strftime
%global debug_package %{nil}

%global goipath         github.com/lestrrat-go/strftime
Version:                1.0.5

%gometa

%global common_description %{expand:
Fast strftime for Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Fast strftime for Go

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/pkg/errors)

%if %{with check}
# Tests
BuildRequires:  golang(github.com/lestrrat-go/envload)
BuildRequires:  golang(github.com/stretchr/testify/assert)
%endif

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
