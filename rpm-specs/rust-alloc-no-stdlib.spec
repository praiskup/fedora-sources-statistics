# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate alloc-no-stdlib

Name:           rust-alloc-no-stdlib
Version:        2.0.4
Release:        %autorelease
Summary:        Dynamic allocator that may be used with or without the stdlib

License:        BSD-3-Clause
URL:            https://crates.io/crates/alloc-no-stdlib
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * prevent example executable from being installed and shipped
Patch:          alloc-no-stdlib-fix-metadata.diff

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
A dynamic allocator that may be used with or without the stdlib. This
allows a package with nostd to allocate memory dynamically and be used
either with a custom allocator, items on the stack, or by a package that
wishes to simply use Box<>. It also provides options to use calloc or a
mutable global variable for pre-zeroed memory.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%doc %{crate_instdir}/README.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+unsafe-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unsafe-devel %{_description}

This package contains library source intended for building other packages which
use the "unsafe" feature of the "%{crate}" crate.

%files       -n %{name}+unsafe-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
# https://github.com/dropbox/rust-alloc-no-stdlib/pull/8
find -type f -name '*.rs' -executable -exec chmod -x '{}' +
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif

%changelog
%autochangelog