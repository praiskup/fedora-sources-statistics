%bcond_without check

# https://github.com/droundy/goopt
%global debug_package %{nil}

%global goipath         github.com/droundy/goopt
%global commit          0b8effe182da161d81b011aba271507324ecb7ab

%gometa

%global common_description %{expand:
Getopt-like flags package for Go.}

%global golicenses      LICENSE
%global godocs          example README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Getopt-like flags package for Go

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
