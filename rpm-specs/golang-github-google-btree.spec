# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/google/btree
%global goipath         github.com/google/btree
Version:                1.0.1

%gometa

%global common_description %{expand:
This package provides an in-memory B-Tree implementation for Go, useful as an
ordered, mutable data structure.

The API is based off of the wonderful
http://godoc.org/github.com/petar/GoLLRB/llrb, and is meant to allow btree to
act as a drop-in replacement for gollrb trees.}

%global golicenses      LICENSE
%global godocs          README.md

%global gosupfiles glide.lock glide.yaml

Name:           %{goname}
Release:        %autorelease
Summary:        BTree implementation for Go

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}
Source1:        glide.yaml
Source2:        glide.lock

%description
%{common_description}

%gopkg

%prep
%goprep
cp %{S:1} %{S:2} .

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog
