# https://github.com/andybalholm/cascadia
%global goipath         github.com/andybalholm/cascadia
Version:                1.2.0
%global debug_package %{nil}


%gometa

%global common_description %{expand:
The Cascadia package implements CSS selectors for use with the parse trees
produced by the html package.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        CSS selector library in Go

# Upstream license specification: BSD-2-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(golang.org/x/net/html)

%description
%{common_description}

%gopkg

%prep
%goprep

%install
%gopkginstall

%check
%gocheck

%gopkgfiles

%changelog
%autochangelog
