# Generated by go2rpm 1.10.0
%bcond check 1

# https://github.com/aquasecurity/trivy
%global goipath         github.com/aquasecurity/trivy
Version:                0.55.2

%gometa -L

%global common_description %{expand:
Find vulnerabilities, misconfigurations, secrets, SBOM in containers,
Kubernetes, code repositories, clouds and more.}

Name:           trivy
Release:        %autorelease
Summary:        Vulnerability and license scanner

# Generated with go-vendor-tools
License:        Apache-2.0 AND BSD-2-Clause AND BSD-2-Clause-Views AND BSD-3-Clause AND BSL-1.0 AND ISC AND MIT AND MPL-2.0 AND OFL-1.1-RFN AND Unicode-DFS-2016 AND Unlicense AND (Apache-2.0 OR GPL-2.0-or-later)
URL:            %{gourl}
Source0:        %{gosource}
Source1:        trivy-%{version}-vendor.tar.xz
Source2:        go-vendor-tools.toml

BuildRequires:  git-core
BuildRequires:  go-vendor-tools
BuildRequires:  sqlite-devel

%description %{common_description}

%prep
%goprep -A
%setup -q -T -D -a1 %{forgesetupargs}
%autopatch -p1
# Keep in sync with go-vendor-tools.toml
sed -i 's|_ "modernc.org/sqlite"|_ "github.com/mattn/go-sqlite3"|' \
    $(grep -rl '_ "modernc.org/sqlite"' pkg/ cmd/ integration/)

%build
# Set the package version in the binary
# Change go-sqlite3 driver name for compatibility with modernc sqlite
%global our_goldflags %{shrink:
    -X=github.com/aquasecurity/trivy/pkg/version.ver=%{version}
    -X=github.com/mattn/go-sqlite3.driverName=sqlite
}
export GO_LDFLAGS=%{shescape:%our_goldflags}
# Do not use the bundled sqlite
export CGO_CFLAGS="-D USE_LIBSQLITE3=1 %{build_cflags}" CGO_LDFLAGS="-lsqlite3 %{build_ldflags}"
# This package does not build without go modules enabled
%global gomodulesmode GO111MODULE=on
%gobuild -o trivy %{goipath}/cmd/trivy

./trivy completion bash > trivy.bash
./trivy completion fish > trivy.fish
./trivy completion zsh > trivy.zsh

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp trivy               %{buildroot}%{_bindir}/
install -Dpm 0755 trivy.bash %{buildroot}%{bash_completions_dir}/trivy
install -Dpm 0755 trivy.fish %{buildroot}%{fish_completions_dir}/trivy.fish
install -Dpm 0755 trivy.zsh  %{buildroot}%{zsh_completions_dir}/_trivy
%go_vendor_license_install -c %{SOURCE2} -d trivy -D "trivy_path=$(pwd)/trivy"

%check
skiptest() {
    for test in "$@"; do
        awk -i inplace '/^func.*'"${test}"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' \
            $(grep -rl "${test}")
    done
}

%go_vendor_license_check -c %{SOURCE2} -d trivy -D "trivy_path=$(pwd)/trivy"
%if %{with check}
# Disable tests that require WASM, generated code, or networking
rm -v \
    pkg/fanal/artifact/repo/git_test.go \
    pkg/module/module_test.go

%ifarch s390x
skiptest Test_dbWorker_update TestFSCache_GetBlob TestFSCache_MissingBlobs
%endif

# Terraform tests attempt to connect to the terraform registry
find pkg/iac/scanners/terraform*/ -name '*_test.go' -print -delete

export GO_LDFLAGS="-X=github.com/mattn/go-sqlite3.driverName=sqlite"
export CGO_CFLAGS="-D USE_LIBSQLITE3=1" CGO_LDFLAGS="-lsqlite3"
%gotest ./...
%endif

%files -f %{go_vendor_license_filelist}
%doc CONTRIBUTING.md README.md SECURITY.md
%{_bindir}/trivy
%{bash_completions_dir}/trivy
%{fish_completions_dir}/trivy.fish
%{zsh_completions_dir}/_trivy

%changelog
%autochangelog