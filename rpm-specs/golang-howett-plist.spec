# Generated by go2rpm 1.8.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/DHowett/go-plist
%global goipath         howett.net/plist
%global forgeurl        https://github.com/DHowett/go-plist
Version:                1.0.1

%gometa -f

%global common_description %{expand:
A pure Go Apple Property List transcoder.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        A pure Go Apple Property List transcoder

# Upstream license specification: BSD-3-Clause
License:        BSD-2-Clause AND BSD-3-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep
# Requires syscall/js and web assembly deps
# ply is not to be known nessescary so don't package it unless it is
rm -r cmd/

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

