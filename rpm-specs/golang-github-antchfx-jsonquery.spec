# Generated by go2rpm 1.14.0
%bcond check 1
%bcond bootstrap 0

%global debug_package %{nil}
%if %{with bootstrap}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(.*\\)$
%endif

# https://github.com/antchfx/jsonquery
%global goipath         github.com/antchfx/jsonquery
Version:                1.3.5

%gometa -L -f

%global common_description %{expand:
JSON xpath query for Go. Golang XPath query for JSON query.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           golang-github-antchfx-jsonquery
Release:        %autorelease
Summary:        JSON xpath query for Go. Golang XPath query for JSON query

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