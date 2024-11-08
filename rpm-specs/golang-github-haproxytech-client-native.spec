%bcond_without check

# https://github.com/haproxytech/client-native
%global debug_package %{nil}

%global goipath         github.com/haproxytech/client-native
Version:                2.5.3

%gometa

%global goaltipaths     %{goipath}/v2

%global common_description %{expand:
Go client for HAProxy configuration and runtime API.}

%global golicenses      LICENSE
%global godocs          README.md runtime/README.md e2e/README.md\\\
                        specification/README.md specification/copyright.txt

Name:           %{goname}
Release:        %autorelease
Summary:        Go client for HAProxy configuration and runtime API

# Upstream license specification: Apache-2.0
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/go-openapi/errors)
BuildRequires:  golang(github.com/go-openapi/strfmt)
BuildRequires:  golang(github.com/go-openapi/swag)
BuildRequires:  golang(github.com/go-openapi/validate)
BuildRequires:  golang(github.com/google/go-cmp/cmp)
BuildRequires:  golang(github.com/google/renameio)
BuildRequires:  golang(github.com/google/uuid)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/common)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/errors)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/options)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/params)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/parsers)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/parsers/actions)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/parsers/filters)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/parsers/http/actions)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/parsers/stats/settings)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/parsers/tcp/actions)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/parsers/tcp/types)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/spoe)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/spoe/types)
BuildRequires:  golang(github.com/haproxytech/config-parser/v4/types)
BuildRequires:  golang(github.com/kballard/go-shellquote)
BuildRequires:  golang(github.com/mitchellh/mapstructure)
BuildRequires:  golang(github.com/pkg/errors)
BuildRequires:  golang(gopkg.in/yaml.v2)

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/assert)
BuildRequires:  golang(github.com/stretchr/testify/require)
BuildRequires:  golang(github.com/stretchr/testify/suite)
%endif

%description
%{common_description}

%gopkg

%prep
%goprep
mv runtime/README.md README-runtime.md
mv e2e/README.md README-e2e.md
mv specification/README.md README-specification.md

%install
%gopkginstall

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc README.md README-runtime.md README-e2e.md README-specification.md
%doc specification/copyright.txt

%gopkgfiles

%changelog
%autochangelog
