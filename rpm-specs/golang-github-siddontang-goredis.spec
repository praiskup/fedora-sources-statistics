# Generated by go2rpm 1.3
%bcond_without check

%global debug_package %{nil}

# https://github.com/siddontang/goredis
%global goipath         github.com/siddontang/goredis
%global commit          0b4019cbd7b74d182c4b0228bc1ee0a8ae6c8b8d

%gometa

%global common_description %{expand:
A simple redis client.}

%global golicenses      LICENSE garyburd_license

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Simple redis client

# Automatically converted from old format: MIT and ASL 2.0 - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

%if %{with check}
# Tests
BuildRequires:  golang(github.com/alicebob/miniredis)
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