# Generated by go2rpm
%bcond_without check

# https://github.com/shurcooL/vfsgen
%global goipath         github.com/shurcooL/vfsgen
%global commit          0d455de96546f756e8830efeec8dab0f489af135

%gometa

%global common_description %{expand:
Package Vfsgen takes an http.FileSystem (likely at go generate time) and
generates Go code that statically implements the provided http.FileSystem.}

%global golicenses      LICENSE
%global godocs          CONTRIBUTING.md README.md

Name:           %{goname}
Version:        0
Release:        0.19%{?dist}
Summary:        Takes an input http.FileSystem and generates code that statically implements it

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/shurcooL/httpfs/vfsutil)

%description
%{common_description}

%gopkg

%prep
%goprep

%build
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

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
%doc CONTRIBUTING.md README.md
%{_bindir}/*

%gopkgfiles

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 0-0.18
- Rebuild for golang 1.22.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 0-0.12
- Rebuild for CVE-2022-{1705,32148,30631,30633,28131,30635,30632,30630,1962} in
  golang

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.11
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 16:47:01 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.7.20210113git0d455de
- Bump to commit 0d455de96546f756e8830efeec8dab0f489af135

* Sun Aug 02 19:12:04 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.6.20200802git92b8a71
- Bump to commit 92b8a710ab6cab4c09182a1fcf469157bc938f8f

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 15 15:59:45 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.1.20190701git6a9ea43
- Initial package