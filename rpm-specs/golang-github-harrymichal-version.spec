%bcond_without check

# https://github.com/HarryMichal/go-version
%global debug_package %{nil}

%global goipath         github.com/HarryMichal/go-version
Version:                1.0.1

%gometa

%global common_description %{expand:
Version normalizer and comparison library for Go}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Version normalizer and comparison library for Go

License:        MIT
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
