# Generated by go2rpm
%ifnarch ppc64le s390x
%bcond_without check
%endif

%global debug_package %{nil}

# https://github.com/remyoudompheng/bigfft
%global goipath         github.com/remyoudompheng/bigfft
%global commit          eec4a21b6bb01e5c1260ca5e04d0c58e11e20f30

%gometa

%global common_description %{expand:
Big integer multiplication library for Go using Fast Fourier transform.}

%global golicenses      LICENSE
%global godocs          README

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Big integer multiplication library for Go using Fast Fourier transform

# Upstream license specification: BSD-3-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
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