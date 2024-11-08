# Generated by go2rpm 1
%bcond_without check

%global debug_package %{nil}

# https://github.com/cucumber/messages-go
%global goipath         github.com/cucumber/messages-go
Version:                17.1.1

%gometa

%global goaltipaths     github.com/cucumber/messages-go/v17

%global common_description %{expand:
Cucumber Messages for Go (Protocol Buffers).}

%global golicenses      LICENSE

Name:           %{goname}
Release:        %autorelease
Summary:        Cucumber Messages for Go (Protocol Buffers)

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/gofrs/uuid)
BuildRequires:  golang(github.com/gogo/protobuf/io)
BuildRequires:  golang(github.com/gogo/protobuf/jsonpb)
BuildRequires:  golang(github.com/gogo/protobuf/proto)

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/require)
%endif

%description
%{common_description}

%gopkg

%prep
%goprep

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
%autochangelog

