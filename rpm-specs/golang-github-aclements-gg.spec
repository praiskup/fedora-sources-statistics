# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/aclements/go-gg
%global goipath         github.com/aclements/go-gg
%global commit          abd1f791f5ee99465ee7cffe771436379d6cee5a

%gometa

%global common_description %{expand:
Gg is a plotting package for Go inspired by the Grammar of Graphics.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Plotting package for Go

# Upstream license specification: BSD-3-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            %{gourl}
Source0:        %{gosource}
Patch0:         0001-Fix-Sprintf-error-with-time-values.patch
Patch1:         0002-Add-missing-format-in-Fatalf.patch

BuildRequires:  golang(github.com/aclements/go-moremath/fit)
BuildRequires:  golang(github.com/aclements/go-moremath/scale)
BuildRequires:  golang(github.com/aclements/go-moremath/stats)
BuildRequires:  golang(github.com/aclements/go-moremath/vec)
BuildRequires:  golang(github.com/ajstarks/svgo)

%description
%{common_description}

%gopkg

%prep
%goprep
%patch -P0 -p1
%patch -P1 -p1

%install
%gopkginstall

%if %{with check}
%check
# new_test.go fails
# https://github.com/aclements/go-gg/issues/11
%gocheck -d "table"
%endif

%gopkgfiles

%changelog
%autochangelog