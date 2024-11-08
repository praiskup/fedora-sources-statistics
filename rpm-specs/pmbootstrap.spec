# Created by pyp2rpm-3.3.5

Name:           pmbootstrap
Version:        2.3.1
Release:        %autorelease
Summary:        A sophisticated chroot/build/flash tool to develop and install postmarketOS

License:        GPL-3.0-only
URL:            https://www.postmarketos.org
# cannot use %%{pypi_source} due to
# https://gitlab.com/postmarketOS/pmbootstrap/-/issues/2009
Source0:        https://gitlab.com/postmarketOS/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(argcomplete)
# FIXME: once we can run the tests, add this back
# BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)

Requires:       openssl
Requires:       git

%description
Sophisticated chroot/build/flash tool to develop and install postmarketOS.

%prep
%autosetup -n %{name}-%{version}
# Remove bundled egg-info
rm -rf %{name}.egg-info

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l pmb

%check
# cannot run the tests at the moment:
# https://gitlab.com/postmarketOS/pmbootstrap/-/issues/2010
# python3 setup.py test

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
%autochangelog
