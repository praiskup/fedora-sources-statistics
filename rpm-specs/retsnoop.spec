# simfail runs on bare metal but not on Koji
%bcond_with check

%global toolchain clang

# upstream build system requires the use of libbpf and bpftool sources
# see https://github.com/anakryiko/retsnoop/issues/22
%global bpftool_url https://github.com/libbpf/bpftool
%global bpftool_commit 64402b8ea43b2ef62ee8ba71d9b50a5e32603fd2
%global bpftool_shortcommit %(c=%{bpftool_commit}; echo ${c:0:7})
%global bpftool_date 20240716
# see bpftool/src/main.c
%global bpftool_version 7.5.0^%{bpftool_date}git%{bpftool_shortcommit}

%global libbpf_url https://github.com/libbpf/libbpf
%global libbpf_commit 686f600bca59e107af4040d0838ca2b02c14ff50
%global libbpf_shortcommit %(c=%{libbpf_commit}; echo ${c:0:7})
%global libbpf_date 20240710
# <mock-chroot> sh-5.2# ./bpftool/bootstrap/bpftool version
# bpftool v7.5.0
# using libbpf v1.5
%global libbpf_version 1.5^%{libbpf_date}git%{libbpf_shortcommit}

Name:           retsnoop
Version:        0.10.1
Release:        %autorelease
Summary:        A tool for investigating kernel error call stacks

# retsnoop: BSD-2-Clause
# bundled libbpf: LGPL-2.1-only OR BSD-2-Clause
# statically linked rust crates
# taken from %%cargo_license_summary
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0 OR MIT
# MIT
# MIT OR Apache-2.0
# MIT OR Zlib OR Apache-2.0
# Unlicense OR MIT
License:        BSD-2-Clause AND (LGPL-2.1-only OR BSD-2-Clause) AND (Apache-2.0 OR MIT) AND MIT AND (0BSD OR Apache-2.0 OR MIT) AND (MIT OR Unlicense) AND (Apache-2.0 OR MIT OR Zlib)
URL:            https://github.com/anakryiko/retsnoop
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{bpftool_url}/archive/%{bpftool_commit}/bpftool-%{bpftool_version}.tar.gz
Source2:        %{libbpf_url}/archive/%{libbpf_commit}/libbpf-%{libbpf_version}.tar.gz
Source3:        README.Fedora
# Use memmap2 rather than the deprecated memmap
# Based on https://github.com/anakryiko/retsnoop/pull/86
Patch:          %{name}-use-memmap2.diff

# has a Rust component
ExclusiveArch:  %{rust_arches}
# rust syn crate not compiling on 32-bit ARM
ExcludeArch:    armv7hl
# bpftool not compiling on ix86
# we don't ship 32-bit binaries anyway, but it'd be good to test compilation
# once this is fixed https://github.com/libbpf/bpftool/issues/158
ExcludeArch:    %{ix86}

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  make
# libbpf deps
BuildRequires:  elfutils-libelf-devel

# upstream does not support dynamic linking
Provides:       bundled(bpftool) = %{bpftool_version}
Provides:       bundled(libbpf) = %{libbpf_version}

%description
retsnoop is BPF-based tool that is meant to help debugging kernel issues. It
allows to capture call stacks of kernel functions that return errors (NULL or
-Exxx) and emits every such detected call stack, along with the captured
results.


%prep
%autosetup -p1
# provide the bpftool version we specify rather than using git submodule
tar xf %{SOURCE1}
rmdir bpftool
mv bpftool-%{bpftool_commit} bpftool
# same license files as libbpf, no-op

# provide the libbpf version we specify rather than using git submodule
tar xf %{SOURCE2}
rmdir libbpf
mv libbpf-%{libbpf_commit} libbpf
mv libbpf/LICENSE libbpf-LICENSE
mv libbpf/LICENSE.BSD-2-Clause  libbpf-LICENSE.BSD-2-Clause
mv libbpf/LICENSE.LGPL-2.1 libbpf-LICENSE.LGPL-2.1

# README.Fedora
cp -p %{SOURCE3} .

# Rust parts
# the path is hardcoded, make sure Cargo.toml is found in the expected place
ln -s sidecar/Cargo.toml .
# the checksums in the lock file might not match
rm sidecar/Cargo.lock
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires


%build
%if 0%{?fedora} < 36
# this is only called automatically after
# https://www.fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck
%set_build_flags
%endif
cd sidecar
%cargo_build
%{cargo_license_summary}
%{cargo_license} > ../LICENSE.dependencies
cd -
%make_build -C src HOSTCC=clang


%install
%make_install -C src prefix=%{_prefix}


%if %{with check}
%check
./src/simfail -a
%endif


%files
%license LICENSE libbpf-LICENSE*
%license LICENSE.dependencies
%doc README.md README.Fedora
%{_bindir}/retsnoop
%{_bindir}/simfail


%changelog
%autochangelog
