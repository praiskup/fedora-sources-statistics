%bcond_without check
# Tests require network access
%bcond_with network
%global debug_package %{nil}


# https://github.com/muesli/crunchy
%global goipath         github.com/muesli/crunchy
Version:                0.4.0

%gometa

%global common_description %{expand:
Finds common flaws in passwords. Like cracklib, but written in Go.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Finds common flaws in passwords

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/xrash/smetrics)

Recommends: words

%if %{with check}
# Tests
BuildRequires:  words
%endif

%description
%{common_description}

%gopkg

%prep
%goprep

%install
%gopkginstall

%if %{with network}
%if %{with check}
%check
%gocheck
%endif
%endif

%gopkgfiles

%changelog
%autochangelog
