# Generated by go2rpm 1.5.0
%bcond_without check

%global debug_package %{nil}

# https://github.com/open-telemetry/opentelemetry-proto-go
%global goipath         go.opentelemetry.io/proto-0.7
%global forgeurl        https://github.com/open-telemetry/opentelemetry-proto-go
Version:                0.7.0

%gometa

%global common_description %{expand:
Generated code for OpenTelemetry protobuf data model.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Generated code for OpenTelemetry protobuf data model

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/golang/protobuf/descriptor)
BuildRequires:  golang(github.com/golang/protobuf/proto)
BuildRequires:  golang(github.com/grpc-ecosystem/grpc-gateway/runtime)
BuildRequires:  golang(github.com/grpc-ecosystem/grpc-gateway/utilities)
BuildRequires:  golang(google.golang.org/grpc)
BuildRequires:  golang(google.golang.org/grpc/codes)
BuildRequires:  golang(google.golang.org/grpc/grpclog)
BuildRequires:  golang(google.golang.org/grpc/metadata)
BuildRequires:  golang(google.golang.org/grpc/status)
BuildRequires:  golang(google.golang.org/protobuf/reflect/protoreflect)
BuildRequires:  golang(google.golang.org/protobuf/runtime/protoimpl)

%description
%{common_description}

%gopkg

%prep
%goprep
sed -i \
    -e 's|"go.opentelemetry.io/proto|"go.opentelemetry.io/proto-0.7|' \
    $(find . -name '*.go')

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 0.7.0-1
- convert license to SPDX

* Fri Aug 06 2021 Robert-André Mauchin <zebob.m@gmail.com> 0.7.0-1
- Uncommitted changes

* Fri Aug 06 2021 Robert-André Mauchin <zebob.m@gmail.com> 0.9.0-1
- Initial release