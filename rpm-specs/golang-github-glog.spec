# Generated by go2rpm 1.7.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/golang/glog
%global goipath         github.com/golang/glog
Version:                1.0.0

%gometa

%global common_description %{expand:
This is an efficient pure Go implementation of leveled logs in the
manner of the open source C++ package.

By binding methods to booleans it is possible to use the log package
without paying the expense of evaluating the arguments to the log.
Through the -vmodule flag, the package also provides fine-grained
control over logging at the file level.}

%global golicenses      LICENSE
%global godocs          README

Name:           %{goname}
Release:        %autorelease
Summary:        Leveled execution logs for Go

License:        Apache-2.0
URL:            %{gourl}
Source:         %{gosource}

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