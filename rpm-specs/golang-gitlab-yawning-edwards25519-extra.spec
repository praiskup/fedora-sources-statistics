# Generated by go2rpm 1.8.2
%bcond_without check
%global debug_package %{nil}

# https://gitlab.com/yawning/edwards25519-extra
%global goipath         gitlab.com/yawning/edwards25519-extra.git
%global forgeurl        https://gitlab.com/yawning/edwards25519-extra
%global commit          def713fd18e464864613d2b55ef41a21df2c9493

%gometa -f

%global common_description %{expand:
This package provides extensions to the Go standard library's Ed25519 and
curve25519 implementations, primarily extracted from curve25519-voi.
This package is intended for interoperability with the standard library
and the edwards25519 package as much as possible.
}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease -p
Summary:        Extensions to the Go standard library's Ed25519 and curve25519 implementations

License:        BSD-3-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

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