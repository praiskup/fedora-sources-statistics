# Generated by rust2rpm 26
%bcond_without check

# nu tests fail on aarch64 builders where the number of cores (224)
# are really high (RAM: 256 GB).
# use this to reduce the number of CPU threads used so we don't hit
# "too many open files" while not affecting builds on other archs
# that much
# x86_64: 48 CPU, 128 GB RAM; s30x: 3 CPU, 16 GB RAM
%if 0%{?el9}
# constrain_build not available
# just limit the max number of CPUs to use to a known-to-work value
%global _smp_ncpus_max 64
%else
%constrain_build -m 4096
%endif

%global crate nu

Name:           rust-nu
Version:        0.96.1
Release:        %autorelease
Summary:        New type of shell

License:        MIT
URL:            https://crates.io/crates/nu
Source:         %{crates_source}
# Automatically generated patch to strip dependencies and normalize metadata
Patch:          nu-fix-metadata-auto.diff
# Manually created patch for downstream crate metadata changes
# * remove minimum Rust version, only bumped for a Windows CVE
# * drop unused tango-bench dependency and benchmarks
# temporarily downgrade serial_test from 3.1 to 3.0
Patch:          nu-fix-metadata.diff

# OOM when linking. We don't ship binaries on ix86 anyway, exclude it
ExcludeArch:    %{ix86}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
A new type of shell.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
# (Apache-2.0 OR MIT) AND BSD-3-Clause
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# BSD-3-Clause
# BSD-3-Clause AND MIT
# CC-PDDC
# CC0-1.0
# ISC
# MIT
# MIT AND Apache-2.0
# MIT OR Apache-2.0
# MIT OR Apache-2.0 OR Zlib
# MIT OR Zlib OR Apache-2.0
# MIT-0 OR Apache-2.0
# MPL-2.0
# Unlicense OR MIT
# Zlib
# Zlib OR Apache-2.0 OR MIT
License:        MIT AND (Apache-2.0 OR MIT) AND BSD-3-Clause AND Unicode-DFS-2016 AND (0BSD OR MIT OR Apache-2.0) AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND CC-PDDC AND CC0-1.0 AND ISC AND (MIT OR Apache-2.0 OR Zlib) AND (MIT-0 OR Apache-2.0) AND MPL-2.0 AND (Unlicense OR MIT) AND Zlib
# LICENSE.dependencies contains a full license breakdown

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE
%license LICENSE.dependencies
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc README.md
%{_bindir}/nu

%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%cargo_install

%if %{with check}
%check
# * these tests depend on unshipped fixtures
%cargo_test -- -- --skip plugin_persistence:: --skip repl::test_custom_commands::deprecated_boolean_flag --skip repl::test_custom_commands::infinite_mutual_recursion_does_not_panic --skip repl::test_custom_commands::infinite_recursion_does_not_panic --skip repl::test_custom_commands::override_table_eval_file --skip repl::test_env::default_nu_lib_dirs_type --skip repl::test_env::default_nu_plugin_dirs_type --skip repl::test_parser::not_panic_with_recursive_call --skip repl::test_spread::spread_external_args --skip repl::test_spread::spread_non_list_args --skip const_:: --skip eval:: --skip hooks:: --skip modules:: --skip overlays:: --skip parsing:: --skip path:: --skip plugin_persistence:: --skip plugins:: --skip scope:: --skip shell::
%endif

%changelog
%autochangelog