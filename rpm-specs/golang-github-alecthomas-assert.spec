# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/alecthomas/assert
%global goipath github.com/alecthomas/assert
Version:        1.0.0

%gometa

%global common_description %{expand:
This is a fork of stretchr's assertion library that does two things:

 - It makes spotting differences in equality much easier. It uses repr and
   diffmatchpatch to display structural differences in colour.
 - Aborts tests on first assertion failure (the same behaviour as
   stretchr/testify/require).}

%global golicenses      LICENCE.txt
%global godocs          _example README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Fork of stretchr/testify/require that provides much nicer diffs

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/alecthomas/colour)
BuildRequires:  golang(github.com/alecthomas/repr)
BuildRequires:  golang(github.com/sergi/go-diff/diffmatchpatch)

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