# Generated by go2rpm 1.9.0
%bcond_without check
%global debug_package %{nil}
# Avoid noarch package built differently on different architectures
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(golang.org/x/sys/cpu\\)$

# https://github.com/minio/highwayhash
%global goipath         github.com/minio/highwayhash
Version:                1.0.2

%gometa -f


%global common_description %{expand:
Native Go version of HighwayHash with optimized assembly implementations on
Intel and ARM}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Native Go version of HighwayHash

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