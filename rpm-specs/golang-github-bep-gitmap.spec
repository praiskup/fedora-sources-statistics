# Generated by go2rpm
%bcond_without check

%global debug_package %{nil}

# https://github.com/bep/gitmap
%global goipath         github.com/bep/gitmap
Version:                1.1.2

%gometa

%global godevelheader %{expand:
Requires:       git-core}

%global common_description %{expand:
A fairly fast way to create a map from all the filenames to info objects for a
given revision of a Git repo.

This library uses os/exec to talk to Git. There are faster ways to do this by
using some Go Git-lib or C bindings, but that adds dependencies I really don't
want or need.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Create map from filename to info object from revision of a repo

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}
# Skip tests that expect gitmap to be a real clone instead of an archive
Patch0:         0001-Skip-repo-tests.patch

BuildRequires:  git-core

%description
%{common_description}

%gopkg

%prep
%goprep
%patch -P0 -p1

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog