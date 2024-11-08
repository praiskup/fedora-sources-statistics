%bcond check 1

# On some releases and architectures, Koji builders sometimes or always run out
# of memory in the final linking step. This cannot be fixed by adding
# "-C link-args=-Wl,--no-keep-memory" to the RUSTFLAGS (as that seems to have
# no significant effect on memory requirements), nor can it be fixed by
# reducing parallelism with e.g. the %%constrain_build macro (although we do
# need this as well), since nothing else is happening at that point in the
# build. See:
# https://doc.rust-lang.org/rustc/codegen-options/index.html#debuginfo
%global rustflags_debuginfo 1

# As a separate limitation, memory exhaustion can occur on builders with very
# many CPUs. Typical workspace crates peak out at 2-4 GB per rustc invocation.
# The uv crate needs much more memory to compile (see the RUSTFLAGS adjustment
# in %%build), but in practice it is also compiled alone after all the other
# crates have finished, so it does not need to influence (and does not benefit
# from) this setting. Even though some crates will require more than 3GB, the
# average should be below that on many-core systems. Increase as needed.
%constrain_build -m 4096

Name:           uv
Version:        0.4.28
Release:        %autorelease
Summary:        An extremely fast Python package installer and resolver, written in Rust

# The license of the uv project is (MIT OR Apache-2.0), except:
#
# Apache-2.0:
#   - crates/uv-python/src/libc.rs contains code derived from
#     crate(glibc_version)
#
# Apache-2.0 OR BSD-2-Clause:
#   - crates/uv-pep440/ is vendored and forked from crate(pep440_rs)
#   - crates/uv-pep508/ is vendored and forked from crate(pep508_rs)
#   - crates/uv-python/packaging/ is vendored and forked from
#     python3dist(packaging)
#
# (Apache-2.0 OR MIT) AND BSD-3-CLause:
#   - The function wheel_metadata_from_remote_zip in
#     crates/uv-client/src/remote_metadata.rs is vendored and forked from the
#     function lazy_read_wheel_metadata in src/index/lazy_metadata.rs in
#     crate(rattler_installs_packages) and is BSD-3-Clause AND (Apache-2.0 OR
#     MIT): the original routine is BSD-3-CLause, and subsequent modifications
#     are explicitly (Apache-2.0 OR MIT).
#
# MIT
#   - crates/uv-virtualenv/src/activator/ is vendored and forked from
#     python3dist(virtualenv)
#
# Additionally, the following are bundled/forked but happen to be under the
# same (Apache-2.0 OR MIT) terms as uv itself:
#   - crates/uv-extract/src/vendor/cloneable_seekable_reader.rs is vendored and
#     forked from crate(ripunzip)
#
# The following are present in the source but believed not to contribute to the
# licenses of the binary RPMs. Note that ecosystem/ contains only
# pyproject.toml files used for testing, not complete bundled projects.
#
# Apache-2.0:
#   - ecosystem/airflow/
#   - ecosystem/home-assistant-core/
#   - ecosystem/transformers/
#   - ecosystem/warehouse/
# Apache-2.0 OR MIT:
#   - ecosystem/packse/
# BSD-2-Clause-Patent:
#   - ecosystem/github-wikidata-bot/
# BSD-3-Clause:
#   - ecosystem/saleor/
# MIT:
#   - crates/uv-python/fetch-download-metadata.py is derived from
#     https://github.com/mitsuhiko/rye/tree/f9822267a7f00332d15be8551f89a212e7bc9017
#     which was MIT.
#   - ecosystem/black/
#
# Rust crates compiled into the executable contribute additional license terms.
# To obtain the following list of licenses, build the package and note the
# output of %%{cargo_license_summary}. This should automatically include the
# licenses of the following bundled forks:
#   - async_zip, Source100, is MIT.
#   - pubgrub, Source200, is MPL-2.0.
#   - reqwest-middleware/reqwest-retry, Source300, is (MIT OR Apache-2.0)
#   - tl, Source400, is MIT.
#
# (Apache-2.0 OR MIT) AND BSD-3-Clause
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 OR BSD-2-Clause
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR ISC OR MIT
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# BSD-3-Clause
# ISC
# ISC AND MIT AND OpenSSL
# LGPL-3.0-or-later OR MPL-2.0
# MIT
# MIT OR Apache-2.0
# MIT OR Apache-2.0 OR Zlib
# MIT OR LGPL-3.0-or-later
# MIT OR Zlib OR Apache-2.0
# MIT-0 OR Apache-2.0
# MPL-2.0
# Unlicense OR MIT
# Zlib OR Apache-2.0 OR MIT
License:        %{shrink:
                0BSD AND
                (0BSD OR Apache-2.0 OR MIT) AND
                Apache-2.0 AND
                (Apache-2.0 OR BSD-2-Clause) AND
                (Apache-2.0 OR BSD-2-Clause OR MIT) AND
                (Apache-2.0 OR BSL-1.0) AND
                (Apache-2.0 OR ISC OR MIT) AND
                (Apache-2.0 OR MIT) AND
                (Apache-2.0 OR MIT OR Zlib) AND
                (Apache-2.0 OR MIT-0) AND
                (Apache-2.0 WITH LLVM-exception) AND
                (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
                BSD-3-Clause AND
                ISC AND
                (LGPL-3.0-or-later OR MIT) AND
                (LGPL-3.0-or-later OR MPL-2.0) AND
                MIT AND
                (MIT OR Unlicense) AND
                MPL-2.0 AND
                OpenSSL AND
                Unicode-DFS-2016
                }
# LICENSE.dependencies contains a full license breakdown
URL:            https://github.com/astral-sh/uv
Source0:        %{url}/archive/%{version}/uv-%{version}.tar.gz

# Currently, uv must use a fork of async_zip, as explained in:
#   Restore central directory buffering
#   https://github.com/charliermarsh/rs-async-zip/pull/2
# and further discussed in
#   Please consider supporting the current release of async_zip
#   https://github.com/prefix-dev/async_http_range_reader/issues/14
# We therefore bundle the fork as prescribed in
#   https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/#_replacing_git_dependencies
%global async_zip_git https://github.com/charliermarsh/rs-async-zip
%global async_zip_rev 011b24604fa7bc223daaad7712c0694bac8f0a87
%global async_zip_baseversion 0.0.17
%global async_zip_snapdate 20240729
Source100:      %{async_zip_git}/archive/%{async_zip_rev}/rs-async-zip-%{async_zip_rev}.tar.gz

# For the foreseeable future, uv must use a fork of pubgrub, as explained in:
#   Plans for eventually using published pubgrub?
#   https://github.com/astral-sh/uv/issues/3794
# We therefore bundle the fork as prescribed in
#   https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/#_replacing_git_dependencies
%global pubgrub_git https://github.com/astral-sh/pubgrub
%global pubgrub_rev 7243f4faf8e54837aa8a401a18406e7173de4ad5
%global pubgrub_baseversion 0.2.1
%global pubgrub_snapdate 20241017
Source200:      %{pubgrub_git}/archive/%{pubgrub_rev}/pubgrub-%{pubgrub_rev}.tar.gz

# We must use a git snapshot of reqwest-middleware/reqwest-retry because a
# necessary incompatible change (originally carried in a uv-specific fork) is
# now present upstream but has not yet appeared in a release, as described in
#   https://github.com/astral-sh/uv/commit/4b193194858707795b5b64dd479f65ef22fed312
# See issue:
#   Add retries to error message
#   https://github.com/TrueLayer/reqwest-middleware/pull/159
# See also: https://github.com/astral-sh/uv/issues/5588#issuecomment-2257474183
# It should be possible for uv to stop using a snapshot, and for us to stop
# bundling, as soon as these changes appear in a new upstream release.
# For now, we must bundle the snapshot as prescribed in
#   https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/#_replacing_git_dependencies
%global reqwest_middleware_git https://github.com/TrueLayer/reqwest-middleware
%global reqwest_middleware_rev d95ec5a99fcc9a4339e1850d40378bbfe55ab121
%global reqwest_middleware_baseversion 0.3.3
%global reqwest_middleware_snapdate 20241017
%global reqwest_retry_baseversion 0.7.1
Source300:      %{reqwest_middleware_git}/archive/%{reqwest_middleware_rev}/reqwest-middleware-%{reqwest_middleware_rev}.tar.gz

# For the time being, uv must use a fork of tl. See:
#   Path back to using released tl crate dependency?
#   https://github.com/astral-sh/uv/issues/6687
# It should be possible to stop forking and bundling if tl upstream merges and
# releases the following fix:
#   Avoid truncating URLs in unquoted hrefs
#   https://github.com/y21/tl/pull/69
# We therefore bundle the fork as prescribed in
#   https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/#_replacing_git_dependencies
%global tl_git https://github.com/charliermarsh/tl
%global tl_rev 6e25b2ee2513d75385101a8ff9f591ef51f314ec
%global tl_baseversion 0.7.8
%global tl_snapdate 20240825
Source400:      %{tl_git}/archive/%{tl_rev}/tl-%{tl_rev}.tar.gz

# Downstream-only: do not override the default allocator
#
# In https://github.com/astral-sh/uv/pull/399, it was reasonably claimed that
# using tikv-jemallocator improved benchmarks by 10%. However, this would
# require packaging at least the tikv-jemalloc-sys, tikv-jemalloc-ctl, and
# tikv-jemallocator crates, and this is expected to be not quite trivial.
# We use the default allocator for now, and reserve tikv-jemallocaator
# packaging as optional future work.
Patch:          0001-Downstream-only-do-not-override-the-default-allocato.patch

# Downstream-only: Always find the system-wide uv executable
# See discussion in
#   Should uv.find_uv_bin() be able to find /usr/bin/uv?
#   https://github.com/astral-sh/uv/issues/4451
Patch:          0001-Downstream-patch-always-find-the-system-wide-uv-exec.patch

# Downstream-only: use the zlib-ng backend for flate2 on all architectures
#
# Upstream excludes s390x and ppc64le because there are issues with the
# build system for the bundled zlib-ng in the libz-ng-sys crate on those
# platforms, but we have no such issues because we always link the system
# zlib-ng, which works fine on these architectures.
Patch:          0001-Downstream-only-use-the-zlib-ng-backend-for-flate2-o.patch

# This patch is for the forked, bundled pubsub crate.
#
# Downstream-only: Revert "feat: ensure successful round-trip of RON (#193)"
#   This reverts commit 21c6a215432fea9a75b7d15d9a9936af9ccc17cb.
# We will not be packaging an alpha version of rust-ron. We can adjust this
# after ron 0.9.x is released.
Patch200:       0001-Downstream-only-Revert-feat-ensure-successful-round-.patch

# This patch is for the forked, bundled reqwest-middleware crate.
#
# Downstream-only: do not attempt to run doctests from README.md
#
# This patch is copied from the rust-reqwest-middleware package. It is
# justified there as avoiding a circular dependency on rust-reqwest-retry, but
# it turns out that running doctests would also require the reqwest-tracing
# crate, which we do not bundle (and is, as of this writing, not separately
# packaged), so the patch is needed here as well.
Patch300:       0001-Downstream-only-do-not-attempt-to-run-doctests-from-.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  rust2rpm-helper
BuildRequires:  tomcli
BuildRequires:  python3-devel

# This is a fork of async_zip; see the notes about Source100.
%global async_zip_snapinfo %{async_zip_snapdate}git%{sub %{async_zip_rev} 1 7}
%global async_zip_version %{async_zip_baseversion}^%{async_zip_snapinfo}
Provides:       bundled(crate(async_zip)) = %{async_zip_version}
# This is a fork of pubgrub; see the notes about Source200.
%global pubgrub_snapinfo %{pubgrub_snapdate}git%{sub %{pubgrub_rev} 1 7}
%global pubgrub_version %{pubgrub_baseversion}^%{pubgrub_snapinfo}
Provides:       bundled(crate(pubgrub)) = %{pubgrub_version}
# This is a fork of reqwest-middleware/reqwest-retry; see the notes about
# Source300.
%global reqwest_middleware_snapinfo %{reqwest_middleware_snapdate}git%{sub %{reqwest_middleware_rev} 1 7}
%global reqwest_middleware_version %{reqwest_middleware_baseversion}^%{reqwest_middleware_snapinfo}
%global reqwest_retry_version %{reqwest_retry_baseversion}^%{reqwest_middleware_snapinfo}
Provides:       bundled(crate(reqwest-middleware)) = %{reqwest_middleware_version}
Provides:       bundled(crate(reqwest-retry)) = %{reqwest_retry_version}
# This is a fork of tl; see the notes about Source400.
%global tl_snapinfo %{tl_snapdate}git%{sub %{tl_rev} 1 7}
%global tl_version %{tl_baseversion}^%{tl_snapinfo}
Provides:       bundled(crate(tl)) = %{tl_version}

# In https://github.com/astral-sh/uv/issues/5588#issuecomment-2257823242,
# upstream writes “These have diverged significantly and the upstream versions
# are only passively maintained, uv requires these custom versions and can't
# use a system copy.”
#
# crates/uv-pep440/
# Version number from Cargo.toml:
Provides:       bundled(crate(pep440_rs)) = 0.7.0
# crates/uv-pep508/
# Cargo.toml has 0.6.0, but Changelog.md shows 0.7.0, and the source reflects
# the changes for 0.7.0:
Provides:       bundled(crate(pep508_rs)) = 0.7.0
# crates/uv-virtualenv/
# As a whole, this crate is derived from https://github.com/konstin/gourgeist
# 0.0.4, which was published as https://crates.io/crates/gourgeist. It looks
# looks like the project was subsumed into `uv`, and the link to `uv` at
# https://konstin.github.io/gourgeist/ seems to support this, so we consider
# this not to be a real case of bundling, and we do not add:
#   Provides:       bundled(crate(gourgeist)) = 0.0.4

# crates/uv-extract/src/vendor/cloneable_seekable_reader.rs
# Version number is an educated guess based on comparison of file contents,
# cross-checked with timing: the file was first introduced to uv as
# crates/puffin-installer/src/vendor/cloneable_seekable_reader.rs in
# https://github.com/astral-sh/uv/commit/2a846e76b7725633776fd08e04ce8b827bb0580f
# on 2023-10-08, and 0.4.0 was the current release of ripunzip at that time.
Provides:       bundled(crate(ripunzip)) = 0.4.0
# wheel_metadata_from_remote_zip only, in
# crates/uv-client/src/remote_metadata.rs
# Version number is, at the time of this writing, the only release of
# https://github.com/prefix-dev/rip containing the corresponding function
# lazy_read_wheel_metadata in
# (crates/rattler_installs_packages/)src/index/lazy_metadata.rs.
Provides:       bundled(crate(rattler_installs_packages)) = 0.9.0

# crates/uv-python/src/libc.rs
# This is at least partially derived (with changes) from the glibc_version
# crate, https://github.com/delta-incubator/glibc-version-rs. The last commit
# that we can match up with the file in uv is
# 5e1002dc7a3c39c0d72631cc488bef2fc5fea0fb, although it would be equally
# correct to reference any of several slightly later commits.
Provides:       bundled(crate(glibc_version)) = 0.1.2^20221117git5e1002d

# The contents of crates/uv-virtualenv/src/activator/ are a bundled and
# slightly forked copy of a subset of https://pypi.org/project/virtualenv; see
# https://github.com/pypa/virtualenv/tree/main/src/virtualenv/activation.
#
# The same justification for not attempting to unbundle downstream applies as
# for the bundling from python3dist(packaging), below; additionally, some of
# the scripts have been forked. See also:
#   https://github.com/astral-sh/uv/issues/5588#issuecomment-2257474140
#
# The scripts were last updated from virtualenv upstream in
# https://github.com/astral-sh/uv/pull/3376 on 2024-05-04; the latest
# virtualenv release at that time was 20.26.0.
Provides:       bundled(python3dist(virtualenv)) = 20.26

# The contents of crates/uv-python/python/packaging/ are a bundled copy of a
# subset of https://pypi.org/project/packaging.
#
# This was added in
# https://github.com/astral-sh/uv/commit/7964bfbb2bed50a5c7b0650a7b6799a66503a33a,
# the commit message of which helps explain the rationale. In part:
#
#   The architecture of uv does not necessarily match that of the python
#   interpreter. In cross compiling/testing scenarios the operating system can
#   also mismatch. To solve this, we move arch and os detection to python,
#   vendoring the relevant pypa/packaging code, preventing mismatches between
#   what the python interpreter was compiled for and what uv was compiled for.
#
# We cannot use the system package directly because these Python sources are
# compiled into the uv executable, and the binary package does not even depend
# on the system Python interpreter. Patching uv to read the sources from the
# system package at runtime would be much too extreme for a downstream change.
# Copying sources from the system package into the build tree is feasible, but
# – especially considering that the sources are not necessarily executed with
# the system Python interpreter – the risks of deviating from upstream’s tested
# sources would seem to greatly outweigh any possible benefits of such
# “build-time unbundling.” We therefore consider this instance of bundling
# technically necessary. See also:
#   https://github.com/astral-sh/uv/issues/5588#issuecomment-2257474140
#
# README.md has the bundled commit hash, __init__.py has the version number,
# and https://github.com/pypa/packaging/tree/${commit} is the source of the
# snapshot date.
Provides:       bundled(python3dist(packaging)) = 24.1~dev0^20240310gitcc938f9

%global common_description %{expand:
An extremely fast Python package installer and resolver, written in Rust.
Designed as a drop-in replacement for common pip and pip-tools workflows.

Highlights:

  • ⚖️ Drop-in replacement for common pip, pip-tools, and virtualenv commands.
  • ⚡️ 10-100x faster than pip and pip-tools (pip-compile and pip-sync).
  • 💾 Disk-space efficient, with a global cache for dependency deduplication.
  • 🐍 Installable via curl, pip, pipx, etc. uv is a static binary that can be
    installed without Rust or Python.
  • 🧪 Tested at-scale against the top 10,000 PyPI packages.
  • 🖥️ Support for macOS, Linux, and Windows.
  • 🧰 Advanced features such as dependency version overrides and alternative
    resolution strategies.
  • ⁉️ Best-in-class error messages with a conflict-tracking resolver.
  • 🤝 Support for a wide range of advanced pip features, including editable
    installs, Git dependencies, direct URL dependencies, local dependencies,
    constraints, source distributions, HTML and JSON indexes, and more.}

%description %{common_description}


%package -n python3-uv
Summary:        Importable Python module for uv

BuildArch:      noarch

Requires:       uv = %{version}-%{release}

%description -n python3-uv %{common_description}

This package provides an importable Python module for uv.


%prep
%autosetup -N
%autopatch -p1 -M99

# Usage: git2path SELECTOR PATH
# Replace a git dependency with a path dependency in Cargo.toml
git2path() {
  tomcli set Cargo.toml del "${1}.git"
  tomcli set Cargo.toml del "${1}.rev"
  tomcli set Cargo.toml str "${1}.path" "${2}"
}

# See comments above Source100:
%setup -q -T -D -b 100 -n uv-%{version}
# Adding the crate to the workspace (in this case implicitly, by linking it
# under crates/) means %%cargo_generate_buildrequires can handle it correctly.
ln -s '../../rs-async-zip-%{async_zip_rev}' crates/async_zip
git2path workspace.dependencies.async_zip crates/async_zip
pushd crates/async_zip
%autopatch -p1 -m100 -M199
popd
install -t LICENSE.bundled/async_zip -D -p -m 0644 crates/async_zip/LICENSE
# Drop dev-dependencies that are only required for compiling the
# actix-multipart example, and remove it. Note that while “futures” is in this
# section of Cargo.toml, it is in fact also used in a test.
tomcli set crates/async_zip/Cargo.toml del dev-dependencies.actix-multipart
mv crates/async_zip/examples/actix_multipart.rs{,.disabled}
tomcli set crates/async_zip/Cargo.toml del dev-dependencies.actix-web
tomcli set crates/async_zip/Cargo.toml del dev-dependencies.derive_more
tomcli set crates/async_zip/Cargo.toml del dev-dependencies.uuid

# See comments above Source200:
%setup -q -T -D -b 200 -n uv-%{version}
ln -s '../../pubgrub-%{pubgrub_rev}' crates/pubgrub
git2path workspace.dependencies.pubgrub crates/pubgrub
pushd crates/pubgrub
%autopatch -p1 -m200 -M299
popd
install -t LICENSE.bundled/pubgrub -D -p -m 0644 crates/pubgrub/LICENSE
# Drop a benchmark-only dev-dependency.
tomcli set crates/pubgrub/Cargo.toml del dev-dependencies.criterion
# Omit tests requiring varisat; it is not packaged and has significant
# dependencies of its own.
tomcli set crates/pubgrub/Cargo.toml del dev-dependencies.varisat
mv crates/pubgrub/tests/proptest.rs{,.disabled}
mv crates/pubgrub/tests/sat_dependency_provider.rs{,.disabled}

# See comments above Source300:
%setup -q -T -D -b 300 -n uv-%{version}
ln -s '../../reqwest-middleware-%{reqwest_middleware_rev}/reqwest-middleware' \
    crates/reqwest-middleware
pushd crates/reqwest-middleware
%autopatch -p1 -m300 -M399
popd
install -t LICENSE.bundled/reqwest-middleware -D -p -m 0644 \
    crates/reqwest-middleware/LICENSE-*
git2path workspace.dependencies.reqwest-middleware crates/reqwest-middleware
git2path patch.crates-io.reqwest-middleware crates/reqwest-middleware
# These dev-dependencies are not really needed, are not packaged, and do not
# appear in the published crates. We remove the unpacked reqwest-tracing source
# to demonstrate we are not bundling it.
tomcli set crates/reqwest-middleware/Cargo.toml del \
    dev-dependencies.reqwest-tracing
rm -r '../reqwest-middleware-%{reqwest_middleware_rev}/reqwest-tracing'
tomcli set crates/reqwest-middleware/Cargo.toml del dev-dependencies.wiremock
ln -s '../../reqwest-middleware-%{reqwest_middleware_rev}/reqwest-retry' \
    crates/reqwest-retry
install -t LICENSE.bundled/reqwest-retry -D -p -m 0644 \
    crates/reqwest-retry/LICENSE-*
git2path workspace.dependencies.reqwest-retry crates/reqwest-retry
# * It is not practical to run the tests:
# * - wiremock is unpackaged, and requires many other unpackaged crates
tomcli set crates/reqwest-retry/Cargo.toml del dev-dependencies.wiremock
mv crates/reqwest-retry/tests/all/main.rs{,.disabled}

# See comments above Source400:
%setup -q -T -D -b 400 -n uv-%{version}
ln -s '../../tl-%{tl_rev}' crates/tl
git2path workspace.dependencies.tl crates/tl
pushd crates/tl
%autopatch -p1 -m400 -M499
popd
install -t LICENSE.bundled/tl -D -p -m 0644 crates/tl/LICENSE
# Drop a benchmark-only dev-dependency.
tomcli set crates/tl/Cargo.toml del dev-dependencies.criterion

# Collect license files of vendored dependencies in the main source archive
install -t LICENSE.bundled/packaging -D -p -m 0644 \
    crates/uv-python/python/packaging/LICENSE.*
install -t LICENSE.bundled/pep440_rs -D -p -m 0644 crates/uv-pep440/License-*
install -t LICENSE.bundled/pep508_rs -D -p -m 0644 crates/uv-pep508/License-*
install -t LICENSE.bundled/ripunzip -D -p -m 0644 \
    crates/uv-extract/src/vendor/LICENSE
# The original license text from rattler_installs_packages is present in a
# comment, but we want it in a separate file so we can ensure it is present in
# the binary RPM.
install -d LICENSE.bundled/rattler_installs_packages
awk '$2 == "BSD" { out=1 }; $2 == "```" { out=0 }; out' \
    crates/uv-client/src/remote_metadata.rs |
  sed -r 's@^///( |$)@@' |
  tee LICENSE.bundled/rattler_installs_packages/LICENSE
# Similarly for virtualenv. All files in
# crates/uv-virtualenv/src/activator/activate/ have the same license text.
install -d LICENSE.bundled/virtualenv
awk '$1 == "#" { out=1 }; $1 != "#" { out=0; exit }; out' \
    crates/uv-virtualenv/src/activator/activate |
  sed -r 's@^#( |$)@@' |
  tee LICENSE.bundled/virtualenv/LICENSE

# Patch out foreign (e.g. Windows-only) dependencies. Follow symbolic links so
# that we also patch the bundled crates we just finished setting up.
find -L . -type f -name Cargo.toml -print \
    -execdir rust2rpm-helper strip-foreign -o '{}' '{}' ';'

# The uv-trampoline crate (a fork of posy trampolines, from
# https://github.com/njsmith/posy) contains a set of trampoline Windows
# executables for launching Python scripts. We must remove these to prove they
# are not used in the build (and since they are only used on Windows, nothing
# is lost by doing so).
rm -v crates/uv-trampoline/trampolines/*.exe
# Per Cargo.toml, uv-trampoline is excluded from the workspace and not
# compiled because it still requires a nightly compiler. For now, we remove it
# entirely to show that we do not need to document bundling from posy.
rm -rv crates/uv-trampoline

# Do not strip the compiled executable; we need useful debuginfo. Upstream set
# this intentionally, so this change makes sense to keep downstream-only.
tomcli set pyproject.toml false tool.maturin.strip
tomcli set Cargo.toml false profile.release.strip

# Exclude the bench crate from the workspace. We don’t need to build and run
# benchmarks, and it brings in unwanted additional dev dependencies.
tomcli set Cargo.toml append workspace.exclude crates/uv-bench
# The uv-dev crate provides “development utilities for uv,” which should not be
# needed here, and it also brings in extra dependencies that we would prefer to
# do without.
tomcli set Cargo.toml append workspace.exclude crates/uv-dev

# Do not request static linking of liblzma – not even when the performance
# feature is enabled.
tomcli set crates/uv-extract/Cargo.toml lists delitem \
    features.performance 'xz2/static'

# The pypi feature, described as “Introduces a dependency on PyPI,” in practice
# controls whether we build and run tests that want to talk to PyPI. In an
# offline build, we definitely don’t want that, so we remove it from the
# default features.
tomcli set crates/uv/Cargo.toml lists delitem features.default 'pypi'
# Similarly, but for crates.io:
tomcli set crates/uv/Cargo.toml lists delitem features.default 'crates-io'

# Omit tests requiring wiremock; its dependency tree is too large and complex
# to consider packaging it right now. The conditional #[cfg(any())] is always
# false.
sed -r -i 's/^#\[cfg\(test\)\]/#[cfg(any())]\r&/' \
    crates/uv-auth/src/middleware.rs
tomcli set crates/uv-auth/Cargo.toml del dev-dependencies.wiremock

# Integration tests (it crate) all require specific Python interpreter versions
# (down to patch release number), which upstream normally downloads,
# precompiled, into the build area – except for the handful of help::* tests in
# crates/uv/tests/it/help.rs. Some may also require network access.
# -p uv --test it:
mods="${mods-}${mods+|}branching_urls"
mods="${mods-}${mods+|}build_backend"
mods="${mods-}${mods+|}pip_(check|list|show|tree|uninstall)"
mods="${mods-}${mods+|}python_(dir|find|install|pin)"
mods="${mods-}${mods+|}venv"
mods="${mods-}${mods+|}workspace"
comment='Downstream-only: skip, needs specific Python interpreter versions'
sed -r -i "s@mod (${mods});@// ${comment}\n#[cfg(any())]\n&@" \
    crates/uv/tests/it/main.rs

# For unclear reasons, maturin checks for the presence of optional crate
# dependencies that correspond to features we have not enabled. We need to
# patch out those that are not packaged, an unfortunate but straightforward
# hack. See further commentary in %%generate_buildrequires.
tomcli set crates/uv/Cargo.toml del dependencies.axoupdater
tomcli set crates/uv/Cargo.toml del features.self-update
tomcli set crates/uv/Cargo.toml del dependencies.tracing-durations-export

# Loosen some version bounds that were aggressively updated upstream by the
# renovate bot. We retain this comment and the following example even when
# there are currently no dependencies that need to be adjusted.
#
# # foocrate
# #   wanted: 0.2.0
# #   currently packaged: 0.1.2
# #   https://bugzilla.redhat.com/show_bug.cgi?id=1234567
# tomcli set crates/uv/Cargo.toml str dev-dependencies.foocrate.version 0.1.2

# unicode-width
#   wanted: 0.1.13
#   currently packaged: 0.1.12 (or 0.1.13+really0.1.12)
# This is a whole mess: https://github.com/unicode-rs/unicode-width/issues/55,
# https://github.com/unicode-rs/unicode-width/issues/66
#
# Once upstream switches to 0.2.0, https://github.com/astral-sh/uv/pull/7632,
# we will no longer need to patch this; however, for now the upstream change is
# waiting for textwrap to make a release that includes
# https://github.com/mgeisler/textwrap/commit/ef91a27bcf5f4cf50ee12993032b227982ecf52e.
tomcli set Cargo.toml str \
    workspace.dependencies.unicode-width.version '0.1.12'

# mailparse
#   wanted: 0.15.0
#   currently packaged: 0.14.0
#   https://bugzilla.redhat.com/show_bug.cgi?id=2258714
tomcli set Cargo.toml str \
    workspace.dependencies.mailparse.version '>=0.14,<0.16'

# goblin
#   wanted: 0.9.0
#   currently packaged: 0.8.2
#   https://bugzilla.redhat.com/show_bug.cgi?id=2320112
tomcli set Cargo.toml str \
    workspace.dependencies.goblin.version '>=0.8.2,<0.10'

%cargo_prep


%generate_buildrequires
# For unclear reasons, maturin checks for all crate dependencies when it is
# invoked as part of %%pyproject_buildrequires – including those corresponding
# to optional features.
#
# Furthermore, if we do not supply -a to %%cargo_generate_buildrequires, then
# maturin will fail looking for crates like pyo3 (and will still look for
# optional crate dependencies).
#
# Since maturin always checks for dev-dependencies, we need -t so that they are
# generated even when the “check” bcond is disabled.
%cargo_generate_buildrequires -a -t
# These crates are excluded from the workspace – upstream writes:
#   Only used to pull in features, allocators, etc. — we specifically don't
#   want them to be part of a workspace-wide cargo check, cargo clippy, etc.
# – but they are still needed to support features, and the build will fail if
# we do not generate their dependencies, too:
for cratedir in \
    crates/uv-performance-memory-allocator \
    crates/uv-performance-flate2-backend
do
  pushd "${cratedir}" >/dev/null
  %cargo_generate_buildrequires -a -t
  popd >/dev/null
done
%pyproject_buildrequires


%build
%pyproject_wheel

%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

# TODO: Since the --help output interacts well with help2man, use it to
# generate man pages: ideally, a man page for each (sub)command
# cross-referenced appropriately. (There are many subcommands, and this would
# be tedious to do manually.) This should be feasible with the --include option
# to help2man and a bit of scripting, but we choose to ship the initial package
# without man pages and defer this to a later effort.


%install
%pyproject_install
%pyproject_save_files uv

if [ '%{python3_sitearch}' != '%{python3_sitelib}' ]
then
  # Maturin is really designed to build compiled Python extensions, but (when
  # the uv executable is not bundled in the Python package) the uv Python
  # library is actually pure-Python, and the python3-uv subpackage can be
  # noarch. We can’t tell maturin to install to the appropriate site-packages
  # directory, but we can fix the installation path manually.
  install -d %{buildroot}%{python3_sitelib}
  mv %{buildroot}%{python3_sitearch}/uv* %{buildroot}%{python3_sitelib}
  sed -r -i 's@%{python3_sitearch}@%{python3_sitelib}@' %{pyproject_files}
fi

# generate and install shell completions
for cmd in uv uvx
do
  target/rpm/${cmd} --generate-shell-completion bash > ${cmd}.bash
  target/rpm/${cmd} --generate-shell-completion fish > ${cmd}.fish
  target/rpm/${cmd} --generate-shell-completion zsh > _${cmd}

  install -Dpm 0644 ${cmd}.bash -t %{buildroot}/%{bash_completions_dir}
  install -Dpm 0644 ${cmd}.fish -t %{buildroot}/%{fish_completions_dir}
  install -Dpm 0644 _${cmd} -t %{buildroot}/%{zsh_completions_dir}
done


%check
%if %{with check}
# These tests rely on debug assertions, and fail when tests are compiled in
# release mode:
#
# cargo test -p uv-auth --lib:
skip="${skip-} --skip keyring::tests::fetch_url_no_host"
skip="${skip-} --skip keyring::tests::fetch_url_with_no_username"
skip="${skip-} --skip keyring::tests::fetch_url_with_password"

# These tests require specific Python interpreter versions (down to patch
# release number), which upstream normally downloads, precompiled, into the
# build area; they might also require network access.
# -p uv-client --test it:
skip="${skip-} --skip remote_metadata::remote_metadata_with_and_without_cache"

%cargo_test -- -- --exact ${skip-}
%endif

%pyproject_check_import


%files
%license LICENSE-APACHE LICENSE-MIT LICENSE.dependencies LICENSE.bundled/
%doc CHANGELOG.md
%doc README.md
%doc PIP_COMPATIBILITY.md

%{_bindir}/uv
# Equivalent to “uv tool run”:
%{_bindir}/uvx

%{bash_completions_dir}/{uv,uvx}.bash
%{fish_completions_dir}/{uv,uvx}.fish
%{zsh_completions_dir}/_{uv,uvx}


%files -n python3-uv -f %{pyproject_files}


%changelog
%autochangelog
