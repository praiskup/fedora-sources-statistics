# Generated by go2rpm 1.6.0
# Rounding errors
%ifarch x86_64
%bcond_without check
%endif

%global debug_package %{nil}

# https://github.com/gonum/gonum
%global goipath         gonum.org/v1/gonum
%global forgeurl        https://github.com/gonum/gonum
Version:                0.9.3

%gometa

%global common_description %{expand:
Gonum is a set of packages designed to make writing numerical and scientific
algorithms productive, performant, and scalable.

Gonum contains libraries for matrices and linear algebra; statistics,
probability distributions, and sampling; tools for function differentiation,
integration, and optimization; network creation and analysis; and more.}

%global golicenses      LICENSE THIRD_PARTY_LICENSES/Bogaert-LICENSE THIRD_PARTY_LICENSES/Boost-LICENSE THIRD_PARTY_LICENSES/Cephes-LICENSE THIRD_PARTY_LICENSES/Fike-LICENSE THIRD_PARTY_LICENSES/Go-LICENSE THIRD_PARTY_LICENSES/Oxford-LICENSE THIRD_PARTY_LICENSES/Probab-LICENSE THIRD_PARTY_LICENSES/Sun-LICENSE
%global godocs          AUTHORS CONDUCT.md CONTRIBUTING.md CONTRIBUTORS README.md README-*.md

Name:           %{goname}
Release:        %autorelease
Summary:        Set of numeric libraries for Go

# Upstream license specification: MIT and BSD-3-Clause and BSL-1.0
# Automatically converted from old format: MIT and BSD and Boost - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND LicenseRef-Callaway-BSD AND BSL-1.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(golang.org/x/exp/rand)
BuildRequires:  golang(golang.org/x/tools/container/intsets)

%description
%{common_description}

%gopkg

%prep
%goprep
for f in blas diff floats graph integrate lapack mat mathext optimize stat; do
  mv $f/README.md README-$f.md
done


%install
%gopkginstall

%if %{with check}
%check
# https://github.com/gonum/gonum/issues/1775
%gocheck -t graph
%endif

%gopkgfiles

%changelog
%autochangelog