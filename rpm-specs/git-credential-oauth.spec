# Generated by go2rpm 1.8.2
%bcond_without check

# https://github.com/hickford/git-credential-oauth
%global goipath         github.com/hickford/git-credential-oauth
Version:                0.13.2

%gometa -f

%global common_description %{expand:
A Git credential helper that authenticates to GitHub, GitLab, BitBucket and
other forges using OAuth. The first time you push, the helper will open a
browser window to authenticate. Subsequent pushes within the cache timeout
require no interaction.}

%global golicenses      LICENSE.txt
%global godocs          CONTRIBUTING.md README.md

Name:           git-credential-oauth
Release:        %autorelease
Summary:        Git credential helper for GitHub and other forges using OAuth

License:        Apache-2.0
URL:            %{gourl}
Source:         %{gosource}

Enhances: git
Recommends: xdg-utils

%description %{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%build
%gobuild -o %{gobuilddir}/bin/git-credential-oauth %{goipath}

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/
install -m 0755 -vd                     %{buildroot}%{_mandir}/man1
install -m 0644 -vp git-credential-oauth.1 -t %{buildroot}%{_mandir}/man1

%if %{with check}
%check
%gocheck
%endif

%files
%{_mandir}/man1/git-credential-oauth.1*
%license LICENSE.txt
%doc CONTRIBUTING.md README.md
%{_bindir}/git-credential-oauth

%gopkgfiles

%changelog
%autochangelog