# Generated by go2rpm 1.8.1
%bcond_without check

# https://github.com/vbatts/tar-split
%global goipath         github.com/vbatts/tar-split
Version:                0.11.2

%gometa

%global common_description %{expand:
Pristinely disassembling a tar archive, and stashing needed raw bytes and
offsets to reassemble a validating original archive.}

%global golicenses      LICENSE
%global godocs          README.md README-tar-split.md

Name:           %{goname}
Release:        %autorelease
Summary:        Checksum-reproducible tar archives (utility/library)

License:        BSD-3-Clause
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep
mv cmd/tar-split/README.md README-tar-split.md

%generate_buildrequires
%go_generate_buildrequires

%build
%gobuild -o %{gobuilddir}/bin/tar-split %{goipath}/cmd/tar-split

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
%doc README.md README-tar-split.md
%{_bindir}/tar-split

%gopkgfiles

%changelog
%autochangelog