# Generated by go2rpm 1.5.0
%bcond_without check

%global debug_package %{nil}

# https://github.com/charmbracelet/glamour
%global goipath         github.com/charmbracelet/glamour
Version:                0.6.0

%gometa

%global common_description %{expand:
Stylesheet-based markdown rendering for your CLI apps.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Stylesheet-based markdown rendering for your CLI apps

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/alecthomas/chroma)
BuildRequires:  golang(github.com/alecthomas/chroma/quick)
BuildRequires:  golang(github.com/alecthomas/chroma/styles)
BuildRequires:  golang(github.com/microcosm-cc/bluemonday)
BuildRequires:  golang(github.com/muesli/reflow/indent)
BuildRequires:  golang(github.com/muesli/reflow/padding)
BuildRequires:  golang(github.com/muesli/reflow/wordwrap)
BuildRequires:  golang(github.com/muesli/termenv)
BuildRequires:  golang(github.com/olekukonko/tablewriter)
BuildRequires:  golang(github.com/yuin/goldmark)
BuildRequires:  golang(github.com/yuin/goldmark-emoji)
BuildRequires:  golang(github.com/yuin/goldmark-emoji/ast)
BuildRequires:  golang(github.com/yuin/goldmark/ast)
BuildRequires:  golang(github.com/yuin/goldmark/extension)
BuildRequires:  golang(github.com/yuin/goldmark/extension/ast)
BuildRequires:  golang(github.com/yuin/goldmark/parser)
BuildRequires:  golang(github.com/yuin/goldmark/renderer)
BuildRequires:  golang(github.com/yuin/goldmark/util)

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