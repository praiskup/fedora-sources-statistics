# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/shurcooL/httpgzip
%global goipath         github.com/shurcooL/httpgzip
%global commit          320755c1c1b0484e6179c9a5b68aabcc0dae5ac2

%gometa

%global common_description %{expand:
Package httpgzip provides net/http-like primitives that use gzip compression
when serving HTTP requests.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Net/http-like primitives that use gzip compression when serving HTTP requests

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(golang.org/x/net/http/httpguts)

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