# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/dlclark/regexp2
%global goipath         github.com/dlclark/regexp2
Version:                1.4.0

%gometa

%global common_description %{expand:
Regexp2 is a feature-rich RegExp engine for Go. It doesn't have constant time
guarantees like the built-in regexp package, but it allows backtracking and is
compatible with Perl5 and .NET. You'll likely be better off with the RE2 engine
from the regexp package and should only use this if you need to write very
complex patterns or require compatibility with .NET.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Regex engine for Go based on the .NET engine

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