# Generated by go2rpm 1.14.0
%bcond check 1
%bcond bootstrap 0

%global debug_package %{nil}

%if %{with bootstrap}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(.*\\)$
%endif

# https://github.com/rs/zerolog
%global goipath         github.com/rs/zerolog
Version:                1.33.0

%gometa -L

%global common_description %{expand:
The Zerolog package provides a fast and simple logger dedicated to JSON output.

Zerolog's API is designed to provide both a great developer experience and
stunning performance. Its unique chaining API allows zerolog to write JSON (or
CBOR) log events by avoiding allocations and reflection.

Uber's zap library pioneered this approach. Zerolog is taking this concept to
the next level with a simpler to use API and even better performance.}

%global golicenses      LICENSE
%global godocs          README.md README-lint.md README-prettylog.md

Name:           golang-github-rs-zerolog
Release:        %autorelease
Summary:        Zero allocation JSON logger

License:        MIT
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

mv cmd/lint/README.md README-lint.md
mv cmd/prettylog/README.md README-prettylog.md

%if %{without bootstrap}
%generate_buildrequires
%go_generate_buildrequires
%endif

%install
%gopkginstall

%if %{without bootstrap}
%if %{with check}
%check
# journald test requires journald running
%gocheck -d journald
%endif
%endif

%gopkgfiles

%changelog
%autochangelog
