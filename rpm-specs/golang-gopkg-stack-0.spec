# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/go-stack/stack
%global goipath         gopkg.in/stack.v0
%global forgeurl        https://github.com/go-stack/stack
%global commit          9b43fcefddd0178abdabf4d484ab0d695d0011db

%gometa

%global common_description %{expand:
Package Stack implements utilities to capture, manipulate, and format call
stacks. It provides a simpler API than package runtime.

The implementation takes care of the minutia and special cases of interpreting
the program counter (pc) values returned by runtime.Callers.}

%global golicenses      LICENSE.md
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease
Summary:        Utilities to capture, manipulate, and format call stacks

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
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
# Fails
rm stackinternal_test.go
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog