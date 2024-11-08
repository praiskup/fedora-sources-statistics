
%global srcname auth.credential

Name:		python-auth-credential
Version:	1.1
Release:	13%{?dist}
Summary:	Python abstraction of a credential
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:	Apache-2.0
URL:		https://github.com/cern-mig/%{name}
Source0:	http://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python3-devel, python3-setuptools

%global _description\
This module offers an abstraction of a credential, i.e. something that\
can be used to authenticate. It allows the creation and manipulation of\
credentials. In particular, it defines a standard string representation\
(so that credentials can be given to external programs as command line\
options), a standard structured representation (so that credentials can\
be stored in structured configuration files or using JSON) and\
"preparators" that can transform credentials into ready-to-use data for\
well known targets.\
\
The python module auth.credential is compatible with the Perl\
module Authen::Credential.

%description %_description

%package -n python3-auth-credential
Summary:	Python abstraction of a credential

%description -n python3-auth-credential
This module offers an abstraction of a credential, i.e. something that
can be used to authenticate. It allows the creation and manipulation of
credentials. In particular, it defines a standard string representation
(so that credentials can be given to external programs as command line
options), a standard structured representation (so that credentials can
be stored in structured configuration files or using JSON) and
"preparators" that can transform credentials into ready-to-use data for
well known targets.

The python module auth.credential is compatible with the Perl
module Authen::Credential.

%prep
%setup -q -n %{srcname}-%{version}
find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build 
%{__python3} setup.py build

%install
rm -fr $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python3} setup.py test

%files -n python3-auth-credential
%doc LICENSE README.rst CHANGES
%{python3_sitelib}/auth/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1-13
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.1-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.1-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Lionel Cons <lionel.cons@cern.ch> - 1.1-5
- Added setuptools dependency (rhbz #2155028)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov  4 2021 Lionel Cons <lionel.cons@cern.ch> - 1.1-1
- Updated to 1.1 (rhbz #2020219)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0-26
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0-23
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-21
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-20
- Rebuilt for Python 3.8

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0-18
- Subpackage python2-auth-credential has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Jul 23 2018 Lionel Cons <lionel.cons@cern.ch> - 1.0-17
- Fixed building using Python 2 (#1605603).

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0-15
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0-13
- Python 2 binary package renamed to python2-auth-credential
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0-10
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Lionel Cons <lionel.cons@cern.ch> - 1.0-7
- Cleanup the spec file.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Massimo Paladin <massimo.paladin@gmail.com> - 1.0-1
- Upgrading to upstream version 1.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Massimo Paladin <massimo.paladin@gmail.com> - 0.6-1
- Upgrading to latest upstream version 0.6.

* Mon Feb 20 2012 Massimo Paladin <Massimo.Paladin@cern.ch> - 0.5-2
- Making it compliant with guidelines.

* Mon Jan 23 2012 Massimo Paladin <Massimo.Paladin@cern.ch> - 0.5-1
- Initial packaging.
