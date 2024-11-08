# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%global giturl  https://github.com/ocaml-ppx/ppx_deriving

Name:           ocaml-ppx-deriving
Version:        6.0.2
Release:        6%{?dist}
Summary:        Type-driven code generation for OCaml

License:        MIT
URL:            https://ocaml-ppx.github.io/ppx_deriving/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/v%{version}/ppx_deriving-%{version}.tar.gz

BuildRequires:  ocaml >= 4.05.0
BuildRequires:  ocaml-cppo >= 1.1.0
BuildRequires:  ocaml-dune >= 1.6.3
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-ppx-derivers-devel
BuildRequires:  ocaml-ppxlib-devel >= 0.32.0

%description
Deriving is a library simplifying type-driven code generation on OCaml.
It includes a set of useful plugins: show, eq, ord (eq), enum, iter,
map (iter), fold (iter), make, yojson, and protobuf.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-ppx-derivers-devel%{?_isa}
Requires:       ocaml-ppxlib-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n ppx_deriving-%{version} -p1

%build
%dune_build

%install
%dune_install

# Help the debuginfo generator find the source files
cd _build/default
ln -s ../../src/ppx_deriving_main.cppo.ml
ln -s ../../src/api/ppx_deriving.cppo.ml .
ln -s ../../src/runtime/ppx_deriving_runtime.cppo.ml .
ln -s ../../src_plugins/create/ppx_deriving_create.cppo.ml .
ln -s ../../src_plugins/enum/ppx_deriving_enum.cppo.ml .
ln -s ../../src_plugins/eq/ppx_deriving_eq.cppo.ml .
ln -s ../../src_plugins/fold/ppx_deriving_fold.cppo.ml .
ln -s ../../src_plugins/iter/ppx_deriving_iter.cppo.ml .
ln -s ../../src_plugins/make/ppx_deriving_make.cppo.ml .
ln -s ../../src_plugins/map/ppx_deriving_map.cppo.ml .
ln -s ../../src_plugins/ord/ppx_deriving_ord.cppo.ml
ln -s ../../src_plugins/show/ppx_deriving_show.cppo.ml
cd -

%check
%dune_check

%files -f .ofiles
%doc CHANGELOG.md README.md
%license LICENSE.txt

%files devel -f .ofiles-devel

%changelog
* Mon Aug  5 2024 Jerry James <loganjerry@gmail.com> - 6.0.2-6
- Rebuild for ocaml-ppxlib 0.33.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Jerry James <loganjerry@gmail.com> - 6.0.2-4
- Rebuild for ocaml-sexplib0 0.17.0

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 6.0.2-3
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 6.0.2-2
- OCaml 5.2.0 for Fedora 41

* Mon May 27 2024 Jerry James <loganjerry@gmail.com> - 6.0.2-1
- Version 6.0.2

* Tue May  7 2024 Jerry James <loganjerry@gmail.com> - 6.0.1-1
- Version 6.0.1
- Drop all patches

* Fri Feb  2 2024 Jerry James <loganjerry@gmail.com> - 5.2.1-28
- Rebuild for changed ocamlx hashes

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-25
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-24
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-23
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-21
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 5.2.1-20
- Add upstream patches for OCaml 5.0 compatibility

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-19
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov  1 2022 Jerry James <loganjerry@gmail.com> - 5.2.1-17
- Rebuild for ocaml-ppxlib 0.28.0

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 5.2.1-16
- Rebuild for ocaml-ppxlib 0.27.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 5.2.1-14
- Use new OCaml macros

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-14
- OCaml 4.14.0 rebuild

* Mon Feb 28 2022 Jerry James <loganjerry@gmail.com> - 5.2.1-13
- Bump and rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-12
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Jerry James <loganjerry@gmail.com> - 5.2.1-10
- Rebuild for ocaml-ppxlib 0.24.0

* Tue Nov 30 2021 Jerry James <loganjerry@gmail.com> - 5.2.1-9
- Rebuild for ocaml-base 0.15.0

* Tue Oct 05 2021 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-8
- OCaml 4.13.1 build

* Wed Sep  1 2021 Jerry James <loganjerry@gmail.com> - 5.2.1-7
- Rebuild for ocaml-ppxlib 0.23.0

* Thu Jul 29 2021 Jerry James <loganjerry@gmail.com> - 5.2.1-6
- Rebuild for ocaml-ppxlib 0.22.2

* Thu Jul 29 2021 Jerry James <loganjerry@gmail.com> - 5.2.1-5
- Rebuild for changed ocamlx(Dynlink)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Jerry James <loganjerry@gmail.com> - 5.2.1-3
- Rebuild for ocaml-ppxlib 0.22.1

* Mon Mar  1 23:22:46 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 5.2.1-2
- OCaml 4.12.0 build

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 5.2.1-1
- Version 5.2.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 5.1-1
- Version 5.1

* Sat Nov 14 2020 Jerry James <loganjerry@gmail.com> - 4.5-4
- Add runtime requirement on ocaml-result-devel (bz 1896793)

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 4.5-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 4.5-2
- OCaml 4.11.0 rebuild

* Wed Aug  5 2020 Jerry James <loganjerry@gmail.com> - 4.5-1
- Version 4.5
- Drop upstreamed ppx_deriving-4.4.1-ocaml-4.11.patch

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 4.4.1-4
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Wed Apr 22 2020 Richard W.M. Jones <rjones@redhat.com> - 4.4.1-3
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 04 2020 Richard W.M. Jones <rjones@redhat.com> - 4.4.1-2
- Update all OCaml dependencies for RPM 4.16.

* Tue Mar 10 2020 Jerry James <loganjerry@gmail.com> - 4.4.1-1
- Initial RPM
