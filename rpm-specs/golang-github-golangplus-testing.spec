# Generated by go2rpm
%bcond_without check
%bcond_with bootstrap
%global debug_package %{nil}


# https://github.com/golangplus/testing
%global goipath         github.com/golangplus/testing
Version:                1.0.0

%gometa

%global common_description %{expand:
Package Testingp is a plus to standard "testing" package..}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Plus to the standard testing package

# Upstream license specification: BSD-3-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/golangplus/fmt)

%if %{without bootstrap}
%if %{with check}
# Tests
BuildRequires:  golang(github.com/golangplus/bytes)
%endif
%endif

%description
%{common_description}

%gopkg

%prep
%goprep

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
