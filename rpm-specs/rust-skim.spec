# Generated by rust2rpm 26
%bcond_without check

%global crate skim

Name:           rust-skim
Version:        0.10.4
Release:        %autorelease
Summary:        Fuzzy Finder in rust!

License:        MIT
URL:            https://crates.io/crates/skim
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * bump derive_builder dependency from 0.11 to 0.20
# * bump nix dependency from 0.25 to 0.26
# * bump vte dependency from 0.11.0 to 0.13.0
Patch:          skim-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Fuzzy Finder in rust!}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# Apache-2.0 OR MIT
# MIT
# MIT OR Apache-2.0
# MPL-2.0
# Unlicense OR MIT
License:        MIT AND MPL-2.0 AND Unicode-DFS-2016 AND (Apache-2.0 OR MIT) AND (Unlicense OR MIT)
# LICENSE.dependencies contains a full license breakdown

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE
%license shell/LICENSE
%license LICENSE.dependencies
%doc CHANGELOG.md
%doc README.md
%{_bindir}/sk
%{_bindir}/sk-tmux
%{_mandir}/man1/sk.1*
%{_mandir}/man1/sk-tmux.1*
%{_datadir}/skim/
%dir %{_datadir}/vim
%dir %{_datadir}/vim/vimfiles
%dir %{_datadir}/vim/vimfiles/plugin
%{_datadir}/vim/vimfiles/plugin/skim.vim
%dir %{_datadir}/nvim
%dir %{_datadir}/nvim/site
%dir %{_datadir}/nvim/site/plugin
%{_datadir}/nvim/site/plugin/skim.vim
%{bash_completions_dir}/sk.bash
%{zsh_completions_dir}/_sk

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%license %{crate_instdir}/shell/LICENSE
%doc %{crate_instdir}/CHANGELOG.md
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

%package     -n %{name}+cli-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+cli-devel %{_description}

This package contains library source intended for building other packages which
use the "cli" feature of the "%{crate}" crate.

%files       -n %{name}+cli-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep
# clean up interpreters
sed -i -e '/^#!\//, 1d' shell/completion.*
sed -i -e '1d;2i#!/bin/bash' bin/sk-tmux

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%cargo_install
# install tmux wrapper script
install -Dpm0755 -t %{buildroot}%{_bindir} \
  bin/sk-tmux
# install manpages
install -Dpm0644 -t %{buildroot}%{_mandir}/man1 \
  man/man1/*
# install data directory
install -d %{buildroot}%{_datadir}/skim
# install vim plugins
install -Dpm0644 -t %{buildroot}%{_datadir}/vim/vimfiles/plugin \
  plugin/skim.vim
install -Dpm0644 -t %{buildroot}%{_datadir}/nvim/site/plugin \
  plugin/skim.vim
# install shell completions
install -Dpm0644 shell/completion.bash %{buildroot}%{bash_completions_dir}/sk.bash
install -Dpm0644 shell/completion.zsh %{buildroot}%{zsh_completions_dir}/_sk
# install shell key bindings (not enabled)
install -Dpm0644 -t %{buildroot}%{_datadir}/skim/shell \
  shell/key-bindings.*

%if %{with check}
%check
# * integer overflow in test code on 32-bit architectures:
#   https://github.com/lotabout/skim/issues/415
%cargo_test -- -- --skip test_atoi
%endif

%changelog
%autochangelog