# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/rainycape/unidecode
%global goipath         github.com/rainycape/unidecode
%global commit          cb7f23ec59bec0d61b19c56cd88cee3d0cc1870c

%gometa

%global common_description %{expand:
Unicode transliterator in Golang: replaces non-ASCII characters with their
ASCII approximations.}

%global golicenses      LICENSE
%global godocs          README.md table.txt

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Unicode transliterator in Golang

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
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