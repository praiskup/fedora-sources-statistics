# Pass --without tests to skip building composer-cli-tests
%bcond_without tests
# Pass --without signed to skip gpg signed tar.gz (DO NOT DO THAT IN PRODUCTION)
%bcond_without signed

%global goipath         github.com/osbuild/weldr-client/v2

Name:      weldr-client
Version:   35.13
Release:   2%{?dist}
# Upstream license specification: Apache-2.0
License:   Apache-2.0
Summary:   Command line utility to control osbuild-composer

%gometa
Url:       %{gourl}
Source0:   https://github.com/osbuild/weldr-client/releases/download/v%{version}/%{name}-%{version}.tar.gz
%if %{with signed}
Source1:   https://github.com/osbuild/weldr-client/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
Source2:   https://keys.openpgp.org/vks/v1/by-fingerprint/117E8C168EFE3A7F#/gpg-117E8C168EFE3A7F.key
%endif

Obsoletes: composer-cli < 35.0
Provides: composer-cli = %{version}-%{release}

Requires: diffutils

BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
%if 0%{?fedora}
BuildRequires:  golang(github.com/BurntSushi/toml)
BuildRequires:  golang(github.com/spf13/cobra)
# Required for tests and %check
BuildRequires:  golang(github.com/stretchr/testify/assert)
BuildRequires:  golang(github.com/stretchr/testify/require)
%endif

BuildRequires: git-core
BuildRequires: make
BuildRequires: gnupg2


%description
Command line utility to control osbuild-composer

%prep
%if %{with signed}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%if 0%{?rhel}
%forgeautosetup -p1
%else
%goprep
%endif

%build
export LDFLAGS="-X %{goipath}/cmd/composer-cli/root.Version=%{version} "

%if 0%{?rhel}
GO_BUILD_PATH=$PWD/_build
install -m 0755 -vd $(dirname $GO_BUILD_PATH/src/%{goipath})
ln -fs $PWD $GO_BUILD_PATH/src/%{goipath}
cd $GO_BUILD_PATH/src/%{goipath}
install -m 0755 -vd _bin
export PATH=$PWD/_bin${PATH:+:$PATH}
export GOPATH=$GO_BUILD_PATH:%{gopath}
export GOFLAGS=-mod=vendor
%else
export GOPATH="%{gobuilddir}:${GOPATH:+${GOPATH}:}%{?gopath}"
export GO111MODULE=off
%endif
%gobuild -o composer-cli %{goipath}/cmd/composer-cli


## TODO
##make man

%if %{with tests} || 0%{?rhel}
export BUILDTAGS="integration"

# Build test binaries with `go test -c`, so that they can take advantage of
# golang's testing package. The RHEL golang rpm macros don't support building them
# directly. Thus, do it manually, taking care to also include a build id.
#
# On Fedora go modules have already been turned off, and the path set to the one into which
# the golang-* packages install source code.
export LDFLAGS="${LDFLAGS:-} -linkmode=external -compressdwarf=false -B 0x$(od -N 20 -An -tx1 -w100 /dev/urandom | tr -d ' ')"
go test -c -tags=integration -buildmode pie -compiler gc -ldflags="${LDFLAGS}" -o composer-cli-tests %{goipath}/weldr
%endif

%install
make DESTDIR=%{buildroot} install

%if %{with tests} || 0%{?rhel}
make DESTDIR=%{buildroot} install-tests
%endif

%check
%if 0%{?fedora}
export GOPATH="%{gobuilddir}:${GOPATH:+${GOPATH}:}%{?gopath}"
export GO111MODULE=off
%endif

# Run the unit tests
export LDFLAGS="-X %{goipath}/cmd/composer-cli/root.Version=%{version} "
make test


%files
%license LICENSE
%doc examples HACKING.md README.md
%{_bindir}/composer-cli
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/composer-cli
%{_mandir}/man1/composer-cli*

%if %{with tests} || 0%{?rhel}
%package tests
Summary:    Integration tests for composer-cli

Requires: createrepo_c

%description tests
Integration tests to be run on a pristine-dedicated system to test the
composer-cli package.

%files tests
%license LICENSE
%{_libexecdir}/tests/composer-cli/
%endif


%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 35.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 07 2024 Brian C. Lane <bcl@redhat.com> - 35.13-1
- New release: 35.13 (bcl)
- HACKING.md: Reformat code blocks for docusaurus (simon.steinbeiss)
- README: Update code block formatting and drop subtitle (simon.steinbeiss)
- info: Add upload status to the output (bcl)
- info: Fix display of blueprint packages with no version (bcl)
- weldr: Add Stringer interface to Package (bcl)
- compose: Add --wait options to start-ostree (bcl)
- compose: Add --wait options to start command (bcl)
- compose: Add compose wait command (bcl)
- weldr: Add ComposeWait to wait for a compose to finish (bcl)
- build(deps): bump github.com/stretchr/testify from 1.8.4 to 1.9.0 (49699333+dependabot[bot])
- CI: Drop SonarQube in favor of Snyk (jrusz)