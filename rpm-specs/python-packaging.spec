%global pypi_name packaging

# Specify --with bootstrap to build in bootstrap mode
# This mode is needed, because python3-rpm-generators need packaging
%bcond_with bootstrap

# When bootstrapping, the tests and docs are disabled because the dependencies are not yet available.
# We don't want python-pretend in future RHEL, so we disable tests on RHEL as well.
# No reason to ship the documentation in RHEL either, so it is also disabled by default.
%if %{without bootstrap} && %{undefined rhel}
# Specify --without docs to prevent the dependency loop on python-sphinx
# Doc subpackage is disabled because it requires sphinx-toolbox since packaging 24.1
# and that package is not available in Fedora yet.
%bcond_with docs

# Specify --without tests to prevent the dependency loop on python-pytest
%bcond_without tests
%else
%bcond_with docs
%bcond_with tests
%endif

Name:           python-%{pypi_name}
Version:        24.1
Release:        2%{?dist}
Summary:        Core utilities for Python packages

License:        BSD-2-Clause OR Apache-2.0
URL:            https://github.com/pypa/packaging
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  unzip

%if %{with bootstrap}
BuildRequires:  python%{python3_pkgversion}-flit-core
%endif

# Upstream uses nox for testing, we specify the test deps manually as well.
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pretend
%endif
%if %{with docs}
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-furo
%endif


%global _description %{expand:
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.}

%description %_description


%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}

%if %{with bootstrap}
Provides:       python%{python3_pkgversion}dist(packaging) = %{version}
Provides:       python%{python3_version}dist(packaging) = %{version}
Requires:       python(abi) = %{python3_version}
%endif

%description -n python%{python3_pkgversion}-%{pypi_name}  %_description


%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation

%description -n python-%{pypi_name}-doc
Documentation for python-packaging
%endif


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%if %{without bootstrap}
%generate_buildrequires
%pyproject_buildrequires -r
%endif


%build
%if %{with bootstrap}
%{python3} -m flit_core.wheel
%else
%pyproject_wheel
%endif

%if %{with docs}
# generate html docs
sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/
%endif


%install
%if %{with bootstrap}
mkdir -p %{buildroot}%{python3_sitelib}
unzip dist/packaging-%{version}-py3-none-any.whl -d %{buildroot}%{python3_sitelib} -x packaging-%{version}.dist-info/RECORD
echo '%{python3_sitelib}/packaging*' > %{pyproject_files}
%else
%pyproject_install
%pyproject_save_files %{pypi_name}
%endif


%check
%{!?with_bootstrap:%pyproject_check_import}
%if %{with tests}
%pytest
%endif


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst


%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD
%endif


%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Lumír Balhar <lbalhar@redhat.com> - 24.1-1
- Update to 24.1 (rhbz#2291172)

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 24.0-3
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Python Maint <python-maint@redhat.com> - 24.0-2
- Bootstrap for Python 3.13

* Mon Mar 11 2024 Lumír Balhar <lbalhar@redhat.com> - 24.0-1
- Update to 24.0 (rhbz#2268783)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 Miro Hrončok <mhroncok@redhat.com> - 23.2-2
- Use the furo Sphinx theme, as intended upstream

* Mon Oct 02 2023 Lumír Balhar <lbalhar@redhat.com> - 23.2-1
- Update to 23.2 (rhbz#2241653)

* Tue Aug 08 2023 Karolina Surma <ksurma@redhat.com> - 23.1-5
- Declare the license as an SPDX expression

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 23.1-3
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 23.1-2
- Bootstrap for Python 3.12

* Mon Apr 17 2023 Lumír Balhar <lbalhar@redhat.com> - 23.1-1
- Update to 23.1 (rhbz#2186423)

* Fri Feb 03 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 23.0-1
- Update to 23.0.0
- https://fedoraproject.org/wiki/Changes/Update_python-packaging_to_version_22_plus
- Fixes: rhbz#2151743

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 21.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 23 2022 Miro Hrončok <mhroncok@redhat.com> - 21.3-7
- Fix tests on Big Endian builders

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 21.3-5
- Rebuilt for pyparsing-3.0.9

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 21.3-4
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 21.3-3
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 18 2021 Lumír Balhar <lbalhar@redhat.com> - 21.3-1
- Update to 21.3
Resolves: rhbz#2024413

* Mon Nov 01 2021 Lumír Balhar <lbalhar@redhat.com> - 21.2-1
- Update to 21.2
Resolves: rhbz#2018534

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Lumír Balhar <lbalhar@redhat.com> - 21.0-1
- Update to 21.0
Resolves: rhbz#1978925

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 20.9-3
- Rebuilt for Python 3.10

* Tue Jun 01 2021 Python Maint <python-maint@redhat.com> - 20.9-2
- Bootstrap for Python 3.10

* Mon Feb 01 2021 Lumír Balhar <lbalhar@redhat.com> - 20.9-1
- Update to 20.9
Resolves: rhbz#1922545

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Lumír Balhar <lbalhar@redhat.com> - 20.8-1
- Update to 20.8 (#1906985)

* Mon Nov 30 2020 Lumír Balhar <lbalhar@redhat.com> - 20.7-1
- Update to 20.7 (#1902369)

* Fri Oct 02 2020 Miro Hrončok <mhroncok@redhat.com> - 20.4-3
- Drop the dependency on six to make the package lighter

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Lumír Balhar <lbalhar@redhat.com> - 20.4-1
- Update to 20.4 (#1838285)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 20.3-3
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 20.3-2
- Bootstrap for Python 3.9

* Fri Mar 06 2020 Lumír Balhar <lbalhar@redhat.com> - 20.3-1
- Update to 20.3 (#1810738)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Lumír Balhar <lbalhar@redhat.com> - 20.1-1
- Update to 20.1 (#1794865)

* Mon Jan 06 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0-2
- Ignore broken tests

* Mon Jan 06 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0-1
- Update to 20.0 (#1788012)

* Thu Sep 26 2019 Lumír Balhar <lbalhar@redhat.com> - 19.2-1
- New upstream version 19.2 (bz#1742388)

* Mon Sep 23 2019 Lumír Balhar <lbalhar@redhat.com> - 19.0-6
- Remove Python 2 subpackage
- Make spec fedora-specific

* Mon Sep 02 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0-5
- Reduce Python 2 build time dependencies

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Lumír Balhar <lbalhar@redhat.com> - 19.0-1
- New upstream version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Charalampos Stratakis <cstratak@redhat.com> - 17.1-1
- Update to 17.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 16.8-10
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 16.8-9
- Bootstrap for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 16.8-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Lumir Balhar <lbalhar@redhat.com> - 16.8-5
- Epel7 compatible spec/package

* Mon Feb 13 2017 Charalampos Stratakis <cstratak@redhat.com> - 16.8-4
- Rebuild as wheel

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 16.8-2
- Rebuild for Python 3.6

* Wed Nov 02 2016 Lumir Balhar <lbalhar@redhat.com> - 16.8-1
- New upstream version

* Fri Sep 16 2016 Lumir Balhar <lbalhar@redhat.com> - 16.7-1
- Initial package.
