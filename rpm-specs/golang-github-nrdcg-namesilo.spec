%bcond_without check

%global goipath         github.com/nrdcg/namesilo
%global debug_package %{nil}

Version:                0.2.1

%gometa

%global common_description %{expand:
Go library for accessing the Namesilo API.}

%global golicenses      LICENSE
%global godocs          readme.md

Name:           %{goname}
Release:        %autorelease
Summary:        Go library for accessing the Namesilo API
License:        MPL-2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/google/go-querystring/query)

%if %{with check}
BuildRequires:  golang(github.com/stretchr/testify/assert)
BuildRequires:  golang(github.com/stretchr/testify/require)
%endif

%description %{common_description}

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
