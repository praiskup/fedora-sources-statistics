ExcludeArch: %{ix86}
# Generated by rust2rpm 26
%bcond_without check

%global crate cosmic-edit


%global commit 96b2a190d8a93955e93de08471477492aafd46c3
%global shortcommit %{sub %{commit} 1 7}
%global commitdatestring 2024-09-24 09:25:49 -0600
%global commitdate 20240924

Name:           cosmic-edit
Version:        1.0.0~alpha.2
Release:        %autorelease
Summary:        Libcosmic text editor

License:        (0BSD OR MIT OR Apache-2.0) AND MIT AND (MIT OR Apache-2.0 OR CC0-1.0) AND (Zlib OR Apache-2.0 OR MIT) AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND MPL-2.0 AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND Zlib AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND Unicode-3.0 AND (BSD-3-Clause OR MIT OR Apache-2.0) AND (Apache-2.0 OR MIT) AND (Unlicense OR MIT) AND (MIT OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND GPL-2.0-only AND ISC AND Apache-2.0 AND CC0-1.0 AND GPL-3.0-only AND BSL-1.0 AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND (Apache-2.0  OR  MIT) AND BSD-2-Clause AND BSD-3-Clause

URL:            https://github.com/pop-os/cosmic-edit

Source0:        https://github.com/pop-os/cosmic-edit/archive/%{commit}/cosmic-edit-%{shortcommit}.tar.gz
# To create the below sources:
# * git clone https://github.com/pop-os/cosmic-edit at the specified commit
# * cargo vendor > vendor-config-%%{shortcommit}.toml
# * tar -pczf vendor-%%{shortcommit}.tar.gz vendor
Source1:        vendor-%{shortcommit}.tar.gz
# * mv vendor-config-%%{shortcommit}.toml ..
Source2:        vendor-config-%{shortcommit}.toml


BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rustc
BuildRequires:  lld
BuildRequires:  cargo
BuildRequires:  just
BuildRequires:  libxkbcommon-devel
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme

%global _description %{expand:
%{summary}.}

%description %{_description}

%prep
%autosetup -n %{crate}-%{commit} -p1 -a1
%cargo_prep -N
# Check if .cargo/config.toml exists
if [ -f .cargo/config.toml ]; then
  # If it exists, append the contents of %%{SOURCE2} to .cargo/config.toml
  cat %{SOURCE2} >> .cargo/config.toml
  echo "Appended %{SOURCE2} to .cargo/config.toml"
else
  # If it does not exist, append the contents of %%{SOURCE2} to .cargo/config
  cat %{SOURCE2} >> .cargo/config
  echo "Appended %{SOURCE2} to .cargo/config"
fi

%build
# Set vergen environment variables
export VERGEN_GIT_COMMIT_DATE="date --utc '%{commitdatestring}'"
export VERGEN_GIT_SHA="%{commit}"
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}
sed 's/\(.*\) (.*#\(.*\))/\1+git\2/' -i cargo-vendor.txt

%install
# Set vergen environment variables
export VERGEN_GIT_COMMIT_DATE="date --utc '%{commitdatestring}'"
export VERGEN_GIT_SHA="%{commit}"
just rootdir=%{buildroot} prefix=%{_prefix} install

# COSMIC is not a valid category pre-fedora 41
%if %{defined fedora} && 0%{?fedora} < 41
desktop-file-install \
--remove-category COSMIC \
--add-category X-COSMIC \
--delete-original \
--dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/com.system76.CosmicEdit.desktop
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.system76.CosmicEdit.desktop
%if %{with check}
# Set vergen environment variables
export VERGEN_GIT_COMMIT_DATE="date --utc '%{commitdatestring}'"
export VERGEN_GIT_SHA="%{commit}"
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/cosmic-edit
%{_datadir}/applications/com.system76.CosmicEdit.desktop
%{_metainfodir}/com.system76.CosmicEdit.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/com.system76.CosmicEdit.svg

%changelog
%autochangelog
