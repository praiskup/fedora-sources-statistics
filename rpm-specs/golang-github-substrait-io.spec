# Generated by go2rpm 1.14.0
%bcond check 1
%bcond bootstrap 0

%global debug_package %{nil}

# https://github.com/substrait-io/substrait-go
%global goipath         github.com/substrait-io/substrait-go
Version:                0.4.2

%gometa -L

%global common_description %{expand:
Experimental Go bindings for substrait.}

%global golicenses      LICENSE
%global godocs          README.md

%global gosupfiles     extensions/definitions/*.yaml

Name:           golang-github-substrait-io
Release:        %autorelease
Summary:        Experimental Go bindings for substrait

License:        Apache-2.0
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

%if %{without bootstrap}
%generate_buildrequires
%go_generate_buildrequires
%endif

%install
%gopkginstall

%if %{without bootstrap}
%if %{with check}
%check
%gocheck
%endif
%endif

%gopkgfiles

%changelog
%autochangelog