# Generated by go2rpm 1
%bcond_without check

# https://github.com/direnv/direnv
%global goipath         github.com/direnv/direnv
Version:                2.32.3

%gometa

%global common_description %{expand:
direnv augments existing shells with a new feature that can load and unload
environment variables depending on the current directory.}

%global golicenses      LICENSE
%global godocs          docs CHANGELOG.md README.md version.txt man/direnv-\\\
                        stdlib.1.md man/direnv.toml.1.md man/direnv.1.md

Name:           direnv
Release:        5%{?dist}
Summary:        Per-directory shell configuration tool

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(github.com/BurntSushi/toml)
BuildRequires:  golang(github.com/direnv/go-dotenv)
BuildRequires:  golang(github.com/mattn/go-isatty)
BuildRequires:  golang(golang.org/x/mod/semver)

%description
%{common_description}

%gopkg

%prep
%goprep

%build
%gobuild -o %{gobuilddir}/bin/direnv %{goipath}

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

install -m 0755 -vd         %{buildroot}%{_mandir}/man1
install -m 0644 -vp man/*.1 %{buildroot}%{_mandir}/man1

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc docs CHANGELOG.md README.md version.txt
%{_bindir}/*
%{_mandir}/man1/*

%gopkgfiles

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 2.32.3-4
- Rebuild for golang 1.22.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 20 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.32.3-1
- Update to latest version (#2148314)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 2.32.1-3
- Rebuild for CVE-2022-{1705,32148,30631,30633,28131,30635,30632,30630,1962} in
  golang

* Sat Jul 09 2022 Maxwell G <gotmax@e.email> - 2.32.1-2
- Rebuild for CVE-2022-{24675,28327,29526} in golang

* Wed Jun 22 2022 Ed Marshall <esm@logic.net> - 2.32.1-1
- Update to 2.32.1
- Close; rhbz#2027120

* Fri Jun 17 2022 Robert-André Mauchin <zebob.m@gmail.com> - 2.28.0-5
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Ed Marshall <esm@logic.net> - 2.28.0-2
- Update to 2.28.0
- Close: rhbz#1938419

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan  2 17:52:00 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.27.0-1
- Update to 2.27.0
- Close: rhbz#1911955

* Fri Jan  1 17:53:53 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.26.0-1
- Update to 2.26.0
- Close: rhbz#1911127

* Sat Dec 26 15:34:39 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2.25.2-1
- Update to 2.25.2
- Close: rhbz#1887117
- Close: rhbz#1910775

* Tue Oct 06 2020 Ed Marshall <esm@logic.net> - 2.22.1-1
- Update to 2.22.1

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 08 2020 Ed Marshall <esm@logic.net> - 2.21.3-1
- Update to 2.21.3
- Removed now-unneeded manpage lint fix

* Wed Jan 29 2020 Ed Marshall <esm@logic.net> - 2.21.2-1
- Update to 2.21.2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 26 2020 Ed Marshall <esm@logic.net> - 2.21.1-1
- Update to 2.21.1

* Wed Oct 30 2019 Ed Marshall <esm@logic.net> - 2.20.1-1
- Update to 2.20.1
- Update spec to latest Fedora go packaging guidelines

* Tue Aug 30 2016 Dominic Cleal <dominic@cleal.org> - 2.9.0-2
- Fix make call to use parallel flag macro
- Fix default values of EA/BRs when macros aren't defined

* Wed Jul 20 2016 Dominic Cleal <dominic@cleal.org> - 2.9.0-1
- Initial build for Fedora