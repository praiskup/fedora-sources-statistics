%bcond_without check

%global modname pynacl

Name:           python-%{modname}
Version:        1.5.0
Release:        10%{?dist}
Summary:        Python binding to the Networking and Cryptography (NaCl) library

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://github.com/pyca/pynacl
Source0:        %{url}/archive/%{version}/%{modname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libsodium-devel

%global _description %{expand:
PyNaCl is a Python binding to the Networking and Cryptography library,
a crypto library with the stated goal of improving usability, security
and speed.}

%description %{_description}

%package -n python3-%{modname}
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-%{modname} %{_description}

Python 3 version.

%prep
%autosetup -p1 -n %{modname}-%{version}
# Remove bundled libsodium, to be sure
rm -vrf src/libsodium/

# ARM and s390x is too slow for upstream tests
# See https://bugzilla.redhat.com/show_bug.cgi?id=1594901
# And https://github.com/pyca/pynacl/issues/370
%ifarch s390x %{arm}
sed -i 's/@settings(deadline=1500, max_examples=5)/@settings(deadline=4000, max_examples=5)/' tests/test_pwhash.py
%endif

%generate_buildrequires
%pyproject_buildrequires %{?with_check:-x tests}

%build
export SODIUM_INSTALL=system
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files nacl

%check
%if %{with check}
%pytest
%else
%pyproject_check_import
%endif

%files -n python3-%{modname} -f %{pyproject_files}
%doc README.rst

%changelog
* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.5.0-10
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.5.0-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 Remi Collet <remi@remirepo.net> - 1.5.0-5
- rebuild for new libsodium

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.5.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 31 2022 Major Hayden <major@mhtx.net> - 1.5.0-1
- Update to 1.5.0 (#2038614)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.0-7
- Rebuilt for Python 3.11

* Wed May 11 2022 Carl George <carl@george.computer> - 1.4.0-6
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 26 2020 Damien Ciabrini <dciabrin@redhat.com> - 1.4.0-1
- Update to 1.4.0 (#1840424)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-8
- Rebuilt for Python 3.9

* Mon May 11 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-7
- Fix build with hypothesis 5 (#1830961)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 13 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-5
- Subpackage python2-pynacl has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Yatin Karel <ykarel@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-2
- Rebuilt for Python 3.7
- Prolong the deadline for tests on s390x
- Don't ignore the test results on arm, do the same as on s390x

* Tue Mar 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 02 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Mon Oct 02 2017 Remi Collet <remi@fedoraproject.org> - 1.1.2-4
- rebuild for libsodium

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Thu Mar 16 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-2
- Rebuild for Python 3.6

* Mon Dec 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.1-1
- Initial package
