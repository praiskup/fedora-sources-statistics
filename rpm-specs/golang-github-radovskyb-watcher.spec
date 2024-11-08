%global goipath     github.com/radovskyb/watcher
%global tag         v1.0.7

%global debug_package %{nil}

%gometa

%global common_description %{expand:
watch for files or directory changes without using filesystem events.}

%global golicenses    LICENSE
%global godocs        *.md

Name:       %{goname}
Version:    1.0.7
Release:    %autorelease
Summary:    watch for files or directory changes without using filesystem events
# Automatically converted from old format: BSD - review is highly recommended.
License:    LicenseRef-Callaway-BSD
URL:        %{gourl}
Source:     %{gosource}

BuildRequires: go-rpm-macros

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
