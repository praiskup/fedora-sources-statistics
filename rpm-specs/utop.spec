# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

# The OCaml code is byte compiled, not native compiled, so there are no ELF
# objects in the binary RPM.
%global debug_package %{nil}

%global giturl  https://github.com/ocaml-community/utop

Name:           utop
Version:        2.14.0
Release:        6%{?dist}
Summary:        Improved toplevel for OCaml

License:        BSD-3-Clause
URL:            https://ocaml-community.github.io/utop/
VCS :           git:%{giturl}.git
Source:         %{giturl}/releases/download/%{version}/%{name}-%{version}.tbz

BuildRequires:  ocaml >= 4.11.0
BuildRequires:  ocaml-alcotest-devel
BuildRequires:  ocaml-cppo >= 1.1.2
BuildRequires:  ocaml-dune >= 2.0
BuildRequires:  ocaml-findlib >= 1.7.2
BuildRequires:  ocaml-lambda-term-devel >= 3.1.0
BuildRequires:  ocaml-logs-devel
BuildRequires:  ocaml-lwt-devel
BuildRequires:  ocaml-lwt-react-devel
BuildRequires:  ocaml-react-devel >= 1.0.0
BuildRequires:  ocaml-xdg-devel >= 3.9.0
BuildRequires:  ocaml-zed-devel >= 3.2.0

# for utop.el
BuildRequires:  emacs-nw
BuildRequires:  emacs-tuareg

Provides:       ocaml-%{name}%{?_isa} = %{version}-%{release}

%description
utop is an improved toplevel (i.e., Read-Eval-Print Loop) for
OCaml. It can run in a terminal or in Emacs. It supports line
editing, history, real-time and context sensitive completion,
colors, and more.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-findlib%{?_isa}
Requires:       ocaml-lambda-term-devel%{?_isa}
Requires:       ocaml-logs-devel%{?_isa}
Requires:       ocaml-zed-devel%{?_isa}

%description devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package -n emacs-utop
Summary:        Emacs front end for utop
BuildArch:      noarch
Requires:       emacs(bin) >= %{?_emacs_version}%{!?_emacs_version:0}
Requires:       emacs-tuareg
Recommends:     emacs-company

%description -n emacs-utop
This package contains an Emacs front end for utop, an improved toplevel
for OCaml.

%prep
%autosetup

%build
%dune_build

cd src/top
emacs -batch --no-init-file --no-site-file \
    --eval "(let ((backup-inhibited t)) (loaddefs-generate \".\" \"$PWD/utop-loaddefs.el\"))"
%_emacs_bytecompile utop.el
cd -

%install
%dune_install

# Install the Emacs interface
mkdir -p %{buildroot}%{_emacs_sitestartdir}
cp -p src/top/utop-loaddefs.* %{buildroot}%{_emacs_sitestartdir}
cp -p src/top/utop.elc %{buildroot}%{_emacs_sitelispdir}

%check
%dune_check

%files -f .ofiles
%license LICENSE
%doc README.md CHANGES.md

%files devel -f .ofiles-devel

%files -n emacs-utop
%{_emacs_sitelispdir}/%{name}.el*
%{_emacs_sitestartdir}/%{name}-loaddefs.el*

%changelog
* Tue Oct 08 2024 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-6
- Rebuild for ocaml-lwt 5.8.0

* Fri Aug  9 2024 Jerry James <loganjerry@gmail.com> - 2.14.0-5
- Generate loaddefs instead of deprecated autoloads

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-3
- OCaml 5.2.0 ppc64le fix

* Thu May 30 2024 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-2
- OCaml 5.2.0 for Fedora 41

* Thu May 23 2024 Jerry James <loganjerry@gmail.com> - 2.14.0-1
- Version 2.14.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 2.13.1-6
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.13.1-5
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 2.13.1-4
- OCaml 5.1 rebuild for Fedora 40

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.13.1-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 2.13.1-1
- Version 2.13.1
- Add a %%check script

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 2.9.2-6
- Rebuild OCaml packages for F38

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 2.9.2-4
- Rebuild for ocaml-lwt 5.6.1
- Convert License tag to SPDX

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 2.9.2-2
- Use new OCaml macros

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 2.9.2-2
- OCaml 4.14.0 rebuild

* Thu Jun 16 2022 Jerry James <loganjerry@gmail.com> - 2.9.2-1
- Version 2.9.2

* Wed Apr 27 2022 Jerry James <loganjerry@gmail.com> - 2.9.1-1
- Version 2.9.1

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.9.0-3
- OCaml 4.13.1 rebuild to remove package notes

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Jerry James <loganjerry@gmail.com> - 2.9.0-1
- Version 2.9.0

* Tue Oct 05 2021 Richard W.M. Jones <rjones@redhat.com> - 2.8.0-3
- OCaml 4.13.1 build

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Jerry James <loganjerry@gmail.com> - 2.8.0-1
- Version 2.8.0
- New emacs-utop package to hold the Emacs interface

* Thu Jun  3 2021 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-6
- Rebuild for new ocaml-lwt.

* Mon Mar 15 2021 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-5
- Bump and rebuild for updated ocaml-findlib.

* Mon Mar  1 19:52:15 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-4
- OCaml 4.12.0 build

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 2.7.0-3
- Rebuild for ocaml-lwt 5.4.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Jerry James <loganjerry@gmail.com> - 2.7.0-1
- Version 2.7.0

* Wed Sep 02 2020 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-2
- OCaml 4.11.0 rebuild

* Fri Aug  7 2020 Jerry James <loganjerry@gmail.com> - 2.6.0-1
- Update to 2.6.0
- Add ocaml-lwt-react-devel and ocaml-react-devel BRs
- Drop unneeded ocaml-bisect-ppx, ocaml-seq, and opam-installer BRs

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-3
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Wed Apr 22 2020 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-2
- OCaml 4.11.0 pre-release attempt 2

* Thu Apr 16 2020 Jerry James <loganjerry@gmail.com> - 2.4.3-1
- Update to 2.4.3
- Add ocaml-bisect-ppx-devel BR
- Remove man page manipulations; they are installed where we want them now

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 05 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.4.2-2
- Require -devel packages of lwt and lambda-term for build step

* Wed Oct 16 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.4.2-1
- Update to 2.4.2

* Mon Aug 12 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.3.0-2
- Update build scripts

* Fri Feb 01 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Mon Dec 03 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.2.0-4
- Update URLs

* Mon Dec 03 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.2.0-3
- Rebuild with lambda-term 1.13

* Sun Aug 12 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.2.0-2
- Fix installing man pages

* Sun Jul 15 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 29 2018 Sergey Avseyev <sergey.avseyev@gmail.com> 2.1.0-2
- Rebuild with findlib 1.8.0

* Mon Mar 05 2018 Sergey Avseyev <sergey.avseyev@gmail.com> 2.1.0-1
- Initial packaging.
