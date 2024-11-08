%global pkgname numericalsgps
%global upname  NumericalSgps
%global giturl  https://github.com/gap-packages/numericalsgps

Name:           gap-pkg-%{pkgname}
Version:        1.4.0
Release:        %autorelease
Summary:        Compute with numerical semigroups and affine semigroups

License:        GPL-2.0-or-later
BuildArch:      noarch
# See https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}
URL:            https://gap-packages.github.io/numericalsgps/
VCS:            git:%{giturl}.git
Source:         %{giturl}/releases/download/v%{version}/%{upname}-%{version}.tar.gz

BuildRequires:  gap-devel
BuildRequires:  gap-pkg-autodoc
BuildRequires:  gap-pkg-normalizinterface
BuildRequires:  gap-pkg-singular

Requires:       gap-core

Recommends:     gap-pkg-normalizinterface
Recommends:     gap-pkg-singular

%description
NumericalSgps is a GAP package for computing with Numerical Semigroups.
Features include:

- defining numerical semigroups;
- computing several properties of numerical semigroups, namely:
  multiplicity, Frobenius number, (minimal) system of generators, Apéry
  set, gaps, fundamental gaps, etc.;
- perform several operations on numerical semigroups and ideals, namely:
  intersection, quotient by an integer, decompose into irreducible
  semigroups, add a special gap, ...;
- computing and testing membership to relevant families of numerical
  semigroups.

%package doc
# The content is GPL-2.0-or-later.
# The remaining licenses cover the various fonts embedded in PDFs:
# AMS: OFL-1.1-RFN
# CM: Knuth-CTAN
# CM-Super: GPL-1.0-or-later
# Nimbus: AGPL-3.0-only
# RSFS: LicenseRef-Rsfs
# StandardSymL: GPL-1.0-or-later
License:        GPL-2.0-or-later AND GPL-1.0-or-later AND OFL-1.1-RFN AND Knuth-CTAN AND AGPL-3.0-only AND LicenseRef-Rsfs
Summary:        Documentation for the GAP NumericalSgps package
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains documentation for gap-pkg-%{pkgname}.

%prep
%autosetup -n %{upname}-%{version}

%build
gap makedoc.g

%install
mkdir -p %{buildroot}%{gap_libdir}/pkg/%{upname}/doc
cp -a data gap tst *.g version  %{buildroot}%{gap_libdir}/pkg/%{upname}
%gap_copy_docs -n %{upname}

%check
gap -l '%{buildroot}%{gap_libdir};' tst/testall.g

%files
%doc CHANGES EXAMPLES README.md
%license GPL LICENSE
%dir %{gap_libdir}/pkg/%{upname}/
%{gap_libdir}/pkg/%{upname}/*.g
%{gap_libdir}/pkg/%{upname}/data/
%{gap_libdir}/pkg/%{upname}/gap/
%{gap_libdir}/pkg/%{upname}/tst/
%{gap_libdir}/pkg/%{upname}/version

%files doc
%docdir %{gap_libdir}/pkg/%{upname}/doc/
%{gap_libdir}/pkg/%{upname}/doc/

%changelog
%autochangelog
