ExcludeArch: %{ix86}
# Generated by rust2rpm 26
%bcond_without check


%global commit afdb65677857946b403043f04ca083810639e4e5
%global shortcommit %{sub %{commit} 1 7}
%global commitdatestring 2024-09-23 11:13:21 +0200
%global commitdate 20240923

Name:           cosmic-comp
Version:        1.0.0~alpha.2
Release:        %autorelease
Summary:        Compositor for the COSMIC Desktop Environment

License:        (0BSD OR MIT OR Apache-2.0) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND BSL-1.0 AND (MIT OR Zlib OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND BSD-3-Clause AND GPL-3.0-only AND ISC AND (Zlib OR Apache-2.0 OR MIT) AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND Zlib AND (Apache-2.0 OR BSD-3-Clause) AND MIT AND (MIT OR Apache-2.0 OR CC0-1.0) AND (Apache-2.0 OR MIT) AND Apache-2.0 AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (MIT OR Apache-2.0 OR Zlib) AND MPL-2.0 AND Unicode-3.0 AND BSD-2-Clause AND CC0-1.0 AND (Unlicense OR MIT) AND (BSD-3-Clause OR MIT OR Apache-2.0) AND (MIT OR Apache-2.0)

URL:            https://github.com/pop-os/cosmic-comp

Source0:        https://github.com/pop-os/cosmic-comp/archive/%{commit}/cosmic-comp-%{shortcommit}.tar.gz
# To create the below sources:
# * git clone https://github.com/pop-os/cosmic-comp at the specified commit
# * cargo vendor > vendor-config-%%{shortcommit}.toml
# * tar -pczf vendor-%%{shortcommit}.tar.gz vendor
Source1:        vendor-%{shortcommit}.tar.gz
# * mv vendor-config-%%{shortcommit}.toml ..
Source2:        vendor-config-%{shortcommit}.toml

BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  rustc
BuildRequires:  lld
BuildRequires:  cargo
BuildRequires:  wayland-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libseat-devel
BuildRequires:  libinput-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  pixman-devel
BuildRequires:  make

Requires:       libseat

Recommends:     cosmic-session

%global _description %{expand:
%{summary}.}

%description %{_description}

%prep
%autosetup -n cosmic-comp-%{commit} -p1 -a1
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
make install DESTDIR=%{buildroot} prefix=%{_prefix}

%if %{with check}
%check
# Set vergen environment variables
export VERGEN_GIT_COMMIT_DATE="date --utc '%{commitdatestring}'"
export VERGEN_GIT_SHA="%{commit}"
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%{_bindir}/cosmic-comp
%{_datadir}/cosmic/com.system76.CosmicSettings.Shortcuts/v1/defaults
%{_datadir}/cosmic/com.system76.CosmicSettings.WindowRules/v1/tiling_exception_defaults

%changelog
%autochangelog
