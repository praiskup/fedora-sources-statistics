# Generated by go2rpm 1.14.0
%bcond check 1
%bcond bootstrap 0

%global debug_package %{nil}

# https://github.com/google/google-api-go-client
%global goipath         google.golang.org/api
%global forgeurl        https://github.com/google/google-api-go-client
Version:                0.185.0

%gometa

%global common_description %{expand:
These are auto-generated Go libraries from the Google Discovery Service's JSON
description files of the available "new style" Google APIs.

Due to the auto-generated nature of this collection of libraries, complete APIs
or specific versions can appear or go away without notice. As a result, you
should always locally vendor any API(s) that your code relies upon.

These client libraries are officially supported by Google. However, the
libraries are considered complete and are in maintenance mode. This means that
we will address critical bugs and security issues but will not add any new
features.}

%global golicenses      LICENSE
%global godocs          docs examples AUTHORS CHANGES.md CODE_OF_CONDUCT.md\\\
                        CONTRIBUTING.md CONTRIBUTORS GettingStarted.md\\\
                        README.md RELEASING.md SECURITY.md TODO testing.md


Name:           %{goname}
Release:        %autorelease
Summary:        Auto-generated Google APIs for Go

License:        BSD-3-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

# Remove to avoid extra deps
rm -rf internal/kokoro/

%if %{without bootstrap}
%generate_buildrequires
%go_generate_buildrequires
%endif

%install
%gopkginstall

%if %{without bootstrap}
%if %{with check}
%check
# Disable tests requiring authentication
for test in "TestNewTokenSource" \
            "TestNewClient_WithCredentialFile" \
            "TestNewClient_WithCredentialJSON" \
            "TestAPIs" \
            "TestNewTokenSource_WithCredentialJSON" \
            "TestLogDirectPathMisconfigAttrempDirectPathNotSet" \
            "TestLogDirectPathMisconfigNotOnGCE" "TestNewClient" \
; do
awk -i inplace '/^func.*'"$test"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' $(grep -rl $test)
done
%if 0%{?__isa_bits} == 32
%gocheck -d iterator
%else
%gocheck
%endif
%endif
%endif

%gopkgfiles

%changelog
%autochangelog