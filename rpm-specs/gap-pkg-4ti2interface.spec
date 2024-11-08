%global pkgname 4ti2interface
%global upname  4ti2Interface
%global upver   2023.02-04
%global giturl  https://github.com/homalg-project/homalg_project/

Name:           gap-pkg-%{pkgname}
Version:        %(tr - . <<< %{upver})
Release:        %autorelease
Summary:        GAP interface to 4ti2

License:        GPL-2.0-or-later
BuildArch:      noarch
# See https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}
URL:            https://homalg-project.github.io/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{upname}-%{upver}.tar.gz
# Adapt to the Fedora 4ti2 package use of environment modules
Patch:          %{name}-binaries.patch

BuildRequires:  4ti2
BuildRequires:  gap-devel
BuildRequires:  gap-pkg-autodoc
BuildRequires:  gap-pkg-io

Requires:       4ti2
Requires:       gap-pkg-io

%description
This package is a GAP interface to 4ti2.

%package doc
# The content is GPL-2.0-or-later.
# The remaining licenses cover the various fonts embedded in PDFs:
# CM: Knuth-CTAN
# CM-Super: GPL-1.0-or-later
# Nimbus: AGPL-3.0-only
License:        GPL-2.0-or-later AND GPL-1.0-or-later AND Knuth-CTAN AND AGPL-3.0-only
Summary:        Documentation for the GAP 4ti2Interface package
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains documentation for gap-pkg-%{pkgname}.

%prep
%autosetup -n homalg_project-%{upname}-%{upver}/%{upname} -p1

%build
export LC_ALL=C.UTF-8
gap makedoc.g

%install
mkdir -p %{buildroot}%{gap_libdir}/pkg/%{upname}/doc
cp -a examples gap tst *.g  %{buildroot}%{gap_libdir}/pkg/%{upname}
%gap_copy_docs -n %{upname}

%check
export LC_ALL=C.UTF-8
gap -l "%{buildroot}%{gap_libdir};" tst/testall.g

%files
%doc README.md
%license LICENSE
%dir %{gap_libdir}/pkg/%{upname}/
%{gap_libdir}/pkg/%{upname}/*.g
%{gap_libdir}/pkg/%{upname}/gap/
%{gap_libdir}/pkg/%{upname}/tst/

%files doc
%docdir %{gap_libdir}/pkg/%{upname}/doc/
%docdir %{gap_libdir}/pkg/%{upname}/examples/
%{gap_libdir}/pkg/%{upname}/doc/
%{gap_libdir}/pkg/%{upname}/examples/

%changelog
%autochangelog
