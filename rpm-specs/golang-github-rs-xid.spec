# Generated by go2rpm 1.9.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/rs/xid
%global goipath         github.com/rs/xid
Version:                1.5.0

%gometa

%global common_description %{expand:
Package Xid is a globally unique id generator library, ready to be used safely
directly in your server code.

Xid is using Mongo Object ID algorithm to generate globally unique ids with a
different serialization (base64) to make it shorter when transported as a
string.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Globally unique id generator thought for the web

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
