# generated by cabal-rpm-2.2.1
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Haskell/

Name:           pagure-cli
Version:        0.2.1
Release:        %autorelease
Summary:        Pagure client

License:        GPL-2.0-or-later
Url:            https://hackage.haskell.org/package/%{name}
# Begin cabal-rpm sources:
Source0:        https://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz
# End cabal-rpm sources

# Begin cabal-rpm deps:
BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
BuildRequires:  ghc-aeson-devel
BuildRequires:  ghc-aeson-pretty-devel
BuildRequires:  ghc-base-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-optparse-applicative-devel
BuildRequires:  ghc-pagure-devel
BuildRequires:  ghc-simple-cmd-args-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-unordered-containers-devel
BuildRequires:  ghc-yaml-devel
BuildRequires:  help2man
# End cabal-rpm deps

%description
A command-line Pagure client for querying projects and users.


%prep
# Begin cabal-rpm setup:
%setup -q
# End cabal-rpm setup


%build
# Begin cabal-rpm build:
%ghc_bin_build
# End cabal-rpm build


%install
# Begin cabal-rpm install
%ghc_bin_install

set noclobber
mkdir -p %{buildroot}%{bash_completions_dir}
%{buildroot}%{_bindir}/pagure --bash-completion-script pagure | sed s/filenames/default/ > %{buildroot}%{bash_completions_dir}/pagure

mkdir -p %{buildroot}%{_mandir}/man1/
help2man --no-info %{buildroot}%{_bindir}/pagure > %{buildroot}%{_mandir}/man1/pagure.1
# End cabal-rpm install


%files
# Begin cabal-rpm files:
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/pagure
%{bash_completions_dir}/pagure
%{_mandir}/man1/pagure.1*
# End cabal-rpm files


%changelog
%autochangelog