# Generated by go2rpm 1.9.0
%bcond_without check
%global debug_package %{nil}

# https://github.com/jamesruan/go-rfc1924
%global goipath         github.com/jamesruan/go-rfc1924
%global commit          2767ca7c638f6e6a9e7eb763c2aeba9d393f6062

%gometa

%global common_description %{expand:
RFC1924 base85 encoding.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Version:        0
Release:        %autorelease -p
Summary:        RFC1924 base85 encoding

License:        MIT
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep
%autopatch -p1

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