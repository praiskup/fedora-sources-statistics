# generated by cabal-rpm-2.2.1
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Haskell/

%global pkg_name versions
%global pkgver %{pkg_name}-%{version}
%{?haskell_setup}

# 1 testcase fails on i686: 18446744073709551610.0.0
%ifnarch %{ix86}
%bcond_without tests
%endif

Name:           ghc-%{pkg_name}
Version:        6.0.7
Release:        %autorelease
Summary:        Types and parsers for software version numbers

License:        BSD-3-Clause
Url:            https://hackage.haskell.org/package/%{pkg_name}
# Begin cabal-rpm sources:
Source0:        https://hackage.haskell.org/package/%{pkgver}/%{pkgver}.tar.gz
# End cabal-rpm sources

# Begin cabal-rpm deps:
BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
BuildRequires:  ghc-base-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-hashable-devel
BuildRequires:  ghc-megaparsec-devel
BuildRequires:  ghc-parser-combinators-devel
BuildRequires:  ghc-template-haskell-devel
BuildRequires:  ghc-text-devel
%if %{with ghc_prof}
BuildRequires:  ghc-base-prof
BuildRequires:  ghc-deepseq-prof
BuildRequires:  ghc-hashable-prof
BuildRequires:  ghc-megaparsec-prof
BuildRequires:  ghc-parser-combinators-prof
BuildRequires:  ghc-template-haskell-prof
BuildRequires:  ghc-text-prof
%endif
%if %{with tests}
BuildRequires:  ghc-microlens-devel
BuildRequires:  ghc-tasty-devel
BuildRequires:  ghc-tasty-hunit-devel
%endif
# End cabal-rpm deps

%description
A library for parsing and comparing software version numbers. We like to give
version numbers to our software in a myriad of ways. Some ways follow strict
guidelines for incrementing and comparison. Some follow conventional wisdom and
are generally self-consistent. Some are just plain asinine. This library
provides a means of parsing and comparing /any/ style of versioning, be it a
nice Semantic Version like this:

> 1.2.3-r1+git123

...or a monstrosity like this:

> 2:10.2+0.0093r3+1-1

Please switch to <http://semver.org Semantic Versioning> if you aren't
currently using it. It provides consistency in version incrementing and has the
best constraints on comparisons.

This library implements version '2.0.0' of the SemVer spec.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name}-static%{?_isa} = %{version}-%{release}
%if %{defined ghc_version}
Requires:       ghc-compiler = %{ghc_version}
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the Haskell %{pkg_name} library development files.


%if %{with haddock}
%package doc
Summary:        Haskell %{pkg_name} library documentation
BuildArch:      noarch
Requires:       ghc-filesystem

%description doc
This package provides the Haskell %{pkg_name} library documentation.
%endif


%if %{with ghc_prof}
%package prof
Summary:        Haskell %{pkg_name} profiling library
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Supplements:    (%{name}-devel and ghc-prof)

%description prof
This package provides the Haskell %{pkg_name} profiling library.
%endif


%prep
# Begin cabal-rpm setup:
%setup -q -n %{pkgver}
# End cabal-rpm setup


%build
# Begin cabal-rpm build:
%ghc_lib_build
# End cabal-rpm build


%install
# Begin cabal-rpm install
%ghc_lib_install
# End cabal-rpm install


%check
%if %{with tests}
%cabal_test
%endif


%files -f %{name}.files
# Begin cabal-rpm files:
%license LICENSE
# End cabal-rpm files


%files devel -f %{name}-devel.files
%doc CHANGELOG.md README.md


%if %{with haddock}
%files doc -f %{name}-doc.files
%license LICENSE
%endif


%if %{with ghc_prof}
%files prof -f %{name}-prof.files
%endif


%changelog
%autochangelog