# Generated by go2rpm 1.9.0
%global debug_package %{nil}
%bcond_without check

# https://github.com/containerd/btrfs
%global goipath         github.com/containerd/btrfs/v2
Version:                2.0.0

%gometa

%global common_description %{expand:
Btrfs bindings for Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Btrfs bindings for Go

License:        Apache-2.0
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
