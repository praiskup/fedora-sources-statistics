# Generated by go2rpm 1.7.0
%bcond_without check

# https://github.com/fullstorydev/grpcurl
%global goipath         github.com/fullstorydev/grpcurl
Version:                1.8.7

%gometa

%global goname grpcurl

%global common_description %{expand:
Like cURL, but for gRPC: Command-line tool for interacting with gRPC servers.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        %autorelease
Summary:        Like cURL, but for gRPC: Command-line tool for interacting with gRPC servers

License:        MIT
URL:            %{gourl}
Source:         %{gosource}

%description
%{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%build
%gobuild -o %{gobuilddir}/bin/%{name} %{goipath}/cmd/%{name}

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/*

%gopkgfiles

%changelog
%autochangelog
