Name:           jowl
Version:        2.3.2
Release:        1%{?dist}
Summary:        CLI for JSON operations with Lodash

License:        MIT
URL:            https://jowl.app
Source0:        https://github.com/daxelrod/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# Also at       https://registry.npmjs.org/{name}/-/{name}-{version}.tgz
# however, npmjs.org has a build product which does not contain docs or tests

# The following sources are generated by running
# nodejs-packaging-bundler against Source0:
Source1:        %{name}-%{version}-nm-prod.tgz
Source2:        %{name}-%{version}-nm-dev.tgz
Source3:        %{name}-%{version}-bundled-licenses.txt

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch
Requires:       nodejs
BuildRequires:  nodejs-devel
BuildRequires:  yarnpkg
BuildRequires:  fdupes

%description
Jowl is a command-line filter for JSON expressions that uses plain JavaScript
with Lodash. It takes JSON on standard in, and writes pretty-printed JSON to
standard out.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE3} .
# Setup bundled runtime(prod) node modules
tar xfz %{SOURCE1}
mkdir -p node_modules
pushd node_modules
ln -s ../node_modules_prod/* .
popd

%build
#nothing to do

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{name}
cp -pr package.json src/bin/jowl.js src/lib/ \
    %{buildroot}%{nodejs_sitelib}/%{name}
# Copy over bundled nodejs modules
cp -pr node_modules node_modules_prod \
    %{buildroot}%{nodejs_sitelib}/%{name}

mkdir -p %{buildroot}%{nodejs_sitelib}/%{name}/bin
# Intentionally not a symlink. If it were a symlink, jowl would be unable to find
# its node-modules
install -p -D -m0755 src/bin/jowl.js %{buildroot}%{nodejs_sitelib}/%{name}/bin/jowl
mkdir -p %{buildroot}%{_bindir}
ln -sf %{nodejs_sitelib}/%{name}/bin/jowl %{buildroot}%{_bindir}/jowl

# Fix the shebang because brp-mangle-shebangs fails to detect this properly (rhbz#1998924)
# This is fixed in fc36 and above
sed -e "s|^#!/usr/bin/env node$|#!/usr/bin/node|" \
    -i %{buildroot}%{nodejs_sitelib}/%{name}/bin/jowl \
    -i %{buildroot}%{nodejs_sitelib}/%{name}/jowl.js

%fdupes %{buildroot}%{nodejs_sitelib}/%{name}

%check
# Setup bundled dev node_modules for testing
#   Note: this cannot be in %%prep or the dev node_modules
#            can get pulled into the regular rpm
tar xfz %{SOURCE2}
# Ensure that this dir exists to be a target of the symlink
mkdir -p node_modules_prod/.bin
pushd node_modules
ln -s -f ../node_modules_dev/* .
popd
mkdir -p node_modules/.bin
pushd node_modules/.bin
ln -s ../../node_modules_dev/.bin/* .
popd
# Run tests
yarn run test


%files
%doc docs/reference.md
%license LICENSE %{name}-%{version}-bundled-licenses.txt
%{nodejs_sitelib}/%{name}/
%{_bindir}/jowl


%changelog
* Sun Jul 21 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Tue Jul 16 2024 Daniel Axelrod <git@danonline.net> - 2.3.2-1
- Update to version 2.3.2

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 21 2022 Daniel Axelrod <fedora@danonline.net> - 2.2.0-1
- Package Jowl according to Fedora Packaging Guide