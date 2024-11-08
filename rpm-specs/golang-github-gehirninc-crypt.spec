%bcond_without check

# https://github.com/GehirnInc/crypt
%global debug_package %{nil}

%global goipath         github.com/GehirnInc/crypt
%global commit          bb7000b8a962b094f1ddb4ae071dfcbd6490d2e9

%gometa

%global common_description %{expand:
Pure Go crypt(3) Implementation.}

%global golicenses      LICENSE
%global godocs          AUTHORS.md README.rst

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Pure Go crypt(3) Implementation

# Upstream license specification: BSD-2-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            %{gourl}
Source0:        %{gosource}

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/assert)
%endif

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
