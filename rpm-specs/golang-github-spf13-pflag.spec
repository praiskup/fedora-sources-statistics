# Generated by go2rpm
%bcond_without check
%global debug_package %{nil}

# https://github.com/spf13/pflag
%global goipath         github.com/spf13/pflag
Version:                1.0.5
%global commit          d5e0c0615acee7028e1e2740a11102313be88de1

%gometa

%global common_description %{expand:
pflag is a drop-in replacement for Go's flag package, implementing
POSIX/GNU-style --flags.

pflag is compatible with the GNU extensions to the POSIX recommendations for
command-line options.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Drop-in replacement for Go's flag package, implementing posix/gnu-style --flags

License:        BSD-3-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep

# Workaround flag_test.go test with golang-1.18
sed -e 's/fmt.Println/fmt.Print/' -i flag_test.go

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
