# Generated by go2rpm 1.8.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/NYTimes/gziphandler
%global goipath         github.com/NYTimes/gziphandler
Version:                1.1.1

%gometa

%global common_description %{expand:
This is a tiny Go package which wraps HTTP handlers to transparently gzip the
response body, for clients which support it. Although it's usually simpler to
leave that to a reverse proxy (like nginx or Varnish), this package is useful
when that's undesirable.}

%global golicenses      LICENSE
%global godocs          CODE_OF_CONDUCT.md CONTRIBUTING.md README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Go middleware to gzip HTTP responses

License:        Apache-2.0
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep

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