# Generated by go2rpm 1.8.2
%bcond_without check
%global debug_package %{nil}

# https://github.com/tonistiigi/vt100
%global goipath         github.com/tonistiigi/vt100
%global commit          8066bb97264f56c603341d3fce837bb504e662ef

%gometa

%global common_description %{expand:
An raw-mode vt100 screen reader.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease -p
Summary:        An raw-mode vt100 screen reader

License:        MIT
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep

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