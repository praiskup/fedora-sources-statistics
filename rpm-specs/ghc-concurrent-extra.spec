# generated by cabal-rpm-2.2.1
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Haskell/

%global pkg_name concurrent-extra
%global pkgver %{pkg_name}-%{version}
%{?haskell_setup}

# testsuite missing deps: test-framework test-framework-hunit

Name:           ghc-%{pkg_name}
Version:        0.7.0.12
Release:        %autorelease
Summary:        Extra concurrency primitives

License:        BSD-3-Clause
Url:            https://hackage.haskell.org/package/%{pkg_name}
# Begin cabal-rpm sources:
Source0:        https://hackage.haskell.org/package/%{pkgver}/%{pkgver}.tar.gz
# End cabal-rpm sources

# Begin cabal-rpm deps:
BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
BuildRequires:  ghc-base-devel
BuildRequires:  ghc-stm-devel
BuildRequires:  ghc-unbounded-delays-devel
%if %{with ghc_prof}
BuildRequires:  ghc-base-prof
BuildRequires:  ghc-stm-prof
BuildRequires:  ghc-unbounded-delays-prof
%endif
# End cabal-rpm deps

%description
The 'concurrent-extra' package offers among other things the following
selection of synchronisation primitives:

* 'Broadcast': Wake multiple threads by broadcasting a value.

* 'Event': Wake multiple threads by signaling an event.

* 'Lock': Enforce exclusive access to a resource. Also known as a binary
semaphore or mutex. The package additionally provides an alternative that works
in the 'STM' monad.

* 'RLock': A lock which can be acquired multiple times by the same thread.
Also known as a reentrant mutex.

* 'ReadWriteLock': Multiple-reader, single-writer locks. Used to protect shared
resources which may be concurrently read, but only sequentially written.

* 'ReadWriteVar': Concurrent read, sequential write variables.

Please consult the API documentation of the individual modules for more
detailed information.

This package was inspired by the concurrency libraries of Java and Python.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name}-static%{?_isa} = %{version}-%{release}
%if %{defined ghc_version}
Requires:       ghc-compiler = %{ghc_version}
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the Haskell %{pkg_name} library development
files.


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


%files -f %{name}.files
# Begin cabal-rpm files:
%license LICENSE
# End cabal-rpm files


%files devel -f %{name}-devel.files
%doc README.markdown


%if %{with haddock}
%files doc -f %{name}-doc.files
%license LICENSE
%endif


%if %{with ghc_prof}
%files prof -f %{name}-prof.files
%endif


%changelog
%autochangelog