# Generated by go2rpm 1.9.0
# Tests are broken and need updating due to onpar changes
%bcond_with check
%global debug_package %{nil}

# https://github.com/go-gorp/gorp
%global goipath         github.com/go-gorp/gorp/v3
Version:                3.1.0

%gometa -f


%global goaltipaths     gopkg.in/gorp.v3

%global common_description %{expand:
Go Relational Persistence - an ORM-ish library for Go.}

%global golicenses      LICENSE
%global godocs          CONTRIBUTING.md README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Go Relational Persistence - an ORM-ish library for Go

License:        MIT
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep
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