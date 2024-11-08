%bcond_without check

# https://github.com/lestrrat-go/envload
%global debug_package %{nil}

%global goipath         github.com/lestrrat-go/envload
%global commit          a3eb8ddeffccdbca0eb6dd6cc7c7950c040a6546

%gometa

%global common_description %{expand:
Restore and load environment variables.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Restore and load environment variables

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

%if %{with check}
# Tests
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
