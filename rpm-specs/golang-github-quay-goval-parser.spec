# Generated by go2rpm 1.5.0
%bcond_without check

# https://github.com/quay/goval-parser
%global goipath         github.com/quay/goval-parser
Version:                0.8.6

%gometa

%global common_description %{expand:
OVAL parser written in go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        OVAL parser written in go

# Upstream license specification: BSD-2-Clause
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            %{gourl}
Source0:        %{gosource}

%if %{with check}
# Tests
BuildRequires:  golang(github.com/google/go-cmp/cmp)
%endif

%description
%{common_description}

%gopkg

%prep
%goprep

%build
%gobuild -o %{gobuilddir}/bin/goval-parser %{goipath}

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/*

%gopkgfiles

%changelog
%autochangelog