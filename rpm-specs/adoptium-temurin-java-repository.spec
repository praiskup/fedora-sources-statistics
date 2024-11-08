%global     reponame   %{name}.repo
%global     repodir    %{_sysconfdir}/yum.repos.d
%global     thirdparty %{_prefix}/lib/fedora-third-party/conf.d
# 0/1 may vary in time, and is always enabled to 1 per FESCO exception
%global     enabled_by_default 0

Name:       adoptium-temurin-java-repository
Version:    1
Release:    %autorelease
Summary:    Fedora package repository files for yum and dnf along with gpg public keys

License:    EPL-2.0
URL:        https://adoptium.net/installation/linux/#_centosrhelfedora_instructions
Source0:    LICENSE
Source1:    %{name}.conf
Source2:    %{reponame}
Source3:    README.md

BuildArch:  noarch
# fedora-third-party contains tools to work with 3rd party repos and owns fedora-third-party/conf.d/ directory
Requires:   fedora-third-party


%description
This package adds configuration to add a remote repository
of https://adoptium.net/installation/linux/#_centosrhelfedora_instructions ,
if third-party repositories are enabled on a Fedora Linux system.
This repository contains all JDKS which are live and not available in fedora 
as per https://fedoraproject.org/wiki/Changes/ThirdPartyLegacyJdks .

%prep
cat %{SOURCE2} |  sed "s/^enabled=0/enabled=%{enabled_by_default}/" > %{reponame}

%build

%install
install -D -m0644 %{SOURCE0} %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -D -m0644 %{SOURCE1} -t %{buildroot}%{thirdparty}/
install -D -m0644 %{reponame} -t %{buildroot}%{repodir}/
install -D -m0644 %{SOURCE3} -t %{buildroot}%{_docdir}/%{name}/

%files
%license LICENSE
%{thirdparty}/*
%config %{repodir}/%{reponame}
%doc README.md

%changelog
%autochangelog
