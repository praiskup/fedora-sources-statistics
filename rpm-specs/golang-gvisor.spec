%bcond_without check

# golang(github.com/bazelbuild/rules_go/go/tools/coverdata) is bundled.
# golang(golang.org/x/sys/cpu) is automatically required only on aarch64
# which is a bad thing for noarch packages;
# filtering it out from automatic requires and requiring it explicitly
# (see below).
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(github.com/bazelbuild/rules_go/go/tools/coverdata\\)$|^golang\\(golang.org/x/sys/cpu\\)$


# https://github.com/google/gvisor
%global goipath         gvisor.dev/gvisor
%global forgeurl        https://github.com/google/gvisor
Version:                20240408.0
# taken from the "go" branch (as bazel is not available in fedora)
%global commit          9e5a99b8205044766a6b5267f6207c00fff83250

%global golang_arches   x86_64 aarch64

%global godevelheader %{expand:
# Workaround for architecture-dependent requires for noarch packages.
# Conditionally compiled file requires this only on aarch64.
# filtering it out from automatic requires and requiring it explicitly.
Requires: golang(golang.org/x/sys/cpu)
}

%gometa

%global common_description %{expand:
gVisor is an open-source, OCI-compatible sandbox runtime that provides
a virtualized container environment. It runs containers with a new
user-space kernel, delivering a low overhead container security
solution for high-density applications.

gVisor integrates with Docker, containerd and Kubernetes, making it
easier to improve the security isolation of your containers while
still using familiar tooling. Additionally, gVisor supports a variety
of underlying mechanisms for intercepting application calls, allowing
it to run in diverse host environments, including cloud-hosted virtual
machines.}

%global gosupfiles      ${vendor[@]}

%global golicenses      LICENSE
%global godocs          README.md AUTHORS

Name:           %{goname}
Release:        %autorelease
Summary:        A container sandbox runtime focused on security, efficiency, and ease of use

# Upstream license specification: Apache-2.0
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}
Source1:        https://github.com/bazelbuild/rules_go/raw/master/go/tools/coverdata/coverdata.go
Patch0:         golang-gvisor-copyconsole.patch
Patch1:         golang-gvisor-startshim.patch
Patch2:         golang-gvisor-setscore.patch
Patch3:         golang-gvisor-marshalany.patch

%description
%{common_description}

%gopkg

%prep
%goprep -A
mkdir -p vendor/github.com/bazelbuild/rules_go/go/tools/coverdata/
cp %{S:1} vendor/github.com/bazelbuild/rules_go/go/tools/coverdata/
%autopatch -p1

%generate_buildrequires
(%{go_generate_buildrequires}) | grep -F -v 'golang(github.com/bazelbuild/rules_go/go/tools/coverdata)'

%build
%gobuild -o %{gobuilddir}/bin/runsc %{goipath}/runsc

%install
mapfile -t vendor <<< $(find vendor -type f)
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/*

%gopkgfiles

%changelog
%autochangelog
