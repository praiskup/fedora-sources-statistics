# Generated by go2rpm 1.6.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/petar-dambovaliev/aho-corasick
%global goipath         github.com/petar-dambovaliev/aho-corasick
%global commit          5ab2d9280aa91038648857abfc060fbca964065f

%gometa

%global common_description %{expand:
Efficient string matching in Golang via the aho-corasick algorithm.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease -p
Summary:        Efficient string matching in Golang via the aho-corasick algorithm

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}

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