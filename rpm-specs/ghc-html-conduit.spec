# generated by cabal-rpm-2.2.1
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Haskell/

%global pkg_name html-conduit
%global pkgver %{pkg_name}-%{version}
%{?haskell_setup}

%bcond_with tests

Name:           ghc-%{pkg_name}
Version:        1.3.2.2
Release:        %autorelease
Summary:        Parse HTML documents using xml-conduit datatypes

License:        MIT
Url:            https://hackage.haskell.org/package/%{pkg_name}
# Begin cabal-rpm sources:
Source0:        https://hackage.haskell.org/package/%{pkgver}/%{pkgver}.tar.gz
# End cabal-rpm sources

# Begin cabal-rpm deps:
BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
BuildRequires:  ghc-attoparsec-devel
BuildRequires:  ghc-base-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-conduit-devel
BuildRequires:  ghc-conduit-extra-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-resourcet-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-xml-conduit-devel
BuildRequires:  ghc-xml-types-devel
%if %{with ghc_prof}
BuildRequires:  ghc-attoparsec-prof
BuildRequires:  ghc-base-prof
BuildRequires:  ghc-bytestring-prof
BuildRequires:  ghc-conduit-prof
BuildRequires:  ghc-conduit-extra-prof
BuildRequires:  ghc-containers-prof
BuildRequires:  ghc-resourcet-prof
BuildRequires:  ghc-text-prof
BuildRequires:  ghc-transformers-prof
BuildRequires:  ghc-xml-conduit-prof
BuildRequires:  ghc-xml-types-prof
%endif
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-hspec-devel
%endif
# End cabal-rpm deps

%description
This package uses tagstream-conduit for its parser. It automatically balances
mismatched tags, so that there shouldn't be any parse failures. It does not
handle a full HTML document rendering, such as adding missing html and head
tags. Note that, since version 1.3.1, it uses an inlined copy of
tagstream-conduit with entity decoding bugfixes applied.


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
%license LICENSE-tagstream-conduit
# End cabal-rpm files


%files devel -f %{name}-devel.files
%doc ChangeLog.md README.md


%if %{with haddock}
%files doc -f %{name}-doc.files
%license LICENSE
%license LICENSE-tagstream-conduit
%endif


%if %{with ghc_prof}
%files prof -f %{name}-prof.files
%endif


%changelog
%autochangelog