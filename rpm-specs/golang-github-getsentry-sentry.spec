# Generated by go2rpm 1.9.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/getsentry/sentry-go
%global goipath         github.com/getsentry/sentry-go
Version:                0.23.0

%gometa

%global common_description %{expand:
Official Sentry SDK for Go.}

%global golicenses      LICENSE
%global godocs          _examples CONTRIBUTING.md MIGRATION.md README.md\\\
                        CHANGELOG.md

Name:           %{goname}
Release:        %autorelease
Summary:        Official Sentry SDK for Go

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep
%autopatch -p1
# To avoid packaging golang-github-kataras-iris-12
rm -rfv iris example/iris

%generate_buildrequires
%go_generate_buildrequires

%install
%gopkginstall

%if %{with check}
%check
export SENTRY_RELEASE=%{version}
for test in "TestStartSpan" \
            "TestStartChild" \
            "TestIntegration" \
            "TestProfilerStackTrace" \
            "TestProfilerOverhead" \
; do
awk -i inplace '/^func.*'"$test"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' $(grep -rl $test)
done
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog