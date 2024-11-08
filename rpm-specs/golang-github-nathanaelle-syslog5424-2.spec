%bcond_without check

# https://github.com/nathanaelle/syslog5424
%global debug_package %{nil}

%global goipath         github.com/nathanaelle/syslog5424/v2
%global forgeurl        https://github.com/nathanaelle/syslog5424
Version:                2.0.5

%gometa

%global common_description %{expand:
Log.Logger-friendly RFC-5424 syslog library.}

%global golicenses      LICENSE.txt
%global godocs          ReadMe.md

Name:           %{goname}
Release:        %autorelease
Summary:        Log.Logger-friendly RFC-5424 syslog library

# Upstream license specification: BSD-2-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
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
