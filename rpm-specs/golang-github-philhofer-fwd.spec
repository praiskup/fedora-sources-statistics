# Generated by go2rpm 1.9.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/philhofer/fwd
%global goipath         github.com/philhofer/fwd
Version:                1.1.2

%gometa

%global common_description %{expand:
The fwd package provides a buffered reader and writer. Each has methods that
help improve the encoding/decoding performance of some binary protocols.

The fwd.Writer and fwd.Reader type provide similar functionality to their
counterparts in bufio, plus a few extra utility methods that simplify
read-ahead and write-ahead.}

%global golicenses      LICENSE.md
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Buffered Reader/Writer

License:        MIT
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