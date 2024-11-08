# Created by pyp2rpm-3.3.2
%global pypi_name jaraco_functools
%global pkg_name jaraco-functools
# Fedora doesn't have all the docs deps yet
%bcond_with docs

Name:           python-%{pkg_name}
Version:        4.0.2
Release:        1%{?dist}
Summary:        Functools like those found in stdlib

License:        MIT
URL:            https://github.com/jaraco/jaraco.functools
Source0:        %{pypi_source %{pypi_name}}
BuildArch:      noarch
 
%description
Functools like those found in stdlib

%package -n python3-%{pkg_name}
Summary:       %{summary}

# python3-jaraco is an RPM-only namespace package for jaraco.*
# it does not exists on PyPI and does not provide python3dist(jaraco)
# DO NOT change this dependency to python3dist(jaraco) or similar
Requires:      python3-jaraco

BuildRequires:  python3-devel
BuildConflicts: python3dist(pytest) = 3.7.3
BuildRequires:  python3dist(jaraco-classes)
BuildRequires:  python3dist(pip) >= 3.4
BuildRequires:  python3dist(pytest) >= 3.4
BuildRequires:  python3dist(setuptools)

%{?python_provide:%python_provide python3-%{pkg_name}}

%description -n python3-%{pkg_name}
Functools like those found in stdlib

%if %{with docs}
%package -n python-%{pkg_name}-doc
Summary:        jaraco-functools documentation

BuildRequires:  python3dist(jaraco-packaging) >= 3.2
BuildRequires:  python3dist(rst-linker) >= 1.9
BuildRequires:  python3dist(sphinx)

%description -n python-%{pkg_name}-doc
Documentation for jaraco-functools
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%if %{with docs}
# generate html docs 
PYTHONPATH=${PWD} sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
%pytest

%files -n python3-%{pkg_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/jaraco/functools*
%{python3_sitelib}/jaraco.functools-%{version}.dist-info

%if %{with docs}
%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE
%endif

%changelog
* Mon Jul 15 2024 Dan Radez <dradez@redhat.com> - 4.0.2-1
- update to upstram 4.0.2 rhbz#2297037

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.0.1-2
- Rebuilt for Python 3.13

* Wed Apr 24 2024 Dan Radez <dradez@redhat.com> - 4.0.1-1
- Update to upstream 4.0.1 rhbz#2276015

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 07 2023 Dan Radez <dradez@redhat.com> - 4.0.0-1
- update to 4.0.0 rhbz#2248009

* Fri Sep 08 2023 Dan Radez <dradez@redhat.com> - 3.9.0-1
- update to 3.9.0 rhbz#2235141

* Tue Aug 08 2023 Dan Radez <dradez@redhat.com> - 3.8.1-1
- update to 3.8.1 rhbz#2229532

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 3.8.0-2
- Rebuilt for Python 3.12

* Tue Jun 27 2023 Dan Radez <dradez@redhat.com> - 3.8.0-1
- update to 3.8.0 rhbz#2217823

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 3.7.0-2
- Rebuilt for Python 3.12

* Mon Jun 19 2023 Dan Radez <dradez@redhat.com> - 3.7.0-1
- update to 3.7.0 rhbz#2210935

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.6.0-2
- Rebuilt for Python 3.12

* Wed Feb 22 2023 Dan Radez <dradez@redhat.com> - 3.6.0
- update to 3.6.0 rhbz#2171917

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 05 2022 Miro Hrončok <mhroncok@redhat.com> - 3.5.2-2
- Remove superfluous runtime dependency on python3-toml

* Wed Sep 28 2022 Dan Radez <dan@radez.net> - 3.5.2-1
- update to 3.5.1 - rhbz#2130355

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Dan Radez <dradez@redhat.com> - 3.5.1-1
- update to 3.5.1
- switched from py3 macros to pyproject macros

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.5.0-5
- Rebuilt for Python 3.11

* Thu Feb 10 2022 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-4
- Make the package installable again
- Fixes: rhbz#2053060

* Wed Feb 09 2022 Dan Radez <dradez@redhat.com> - 3.5.0-3
- Don't delete egginfo

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Dan Radez <dradez@redhat.com> - 3.5.0-1
- updating to 3.5.0
- Reenabled checks! Yay \o/

* Mon Dec 06 2021 Dan Radez <dradez@redhat.com> - 3.4.0-1
- updating to 3.4.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.3.0-2
- Rebuilt for Python 3.10

* Fri Apr 30 2021 Dan Radez <dradez@redhat.com> - 3.3.0-1
- updating to 3.3.0

* Tue Feb 23 2021 Dan Radez <dradez@redhat.com> - 3.2.1-1
- updating to 3.2.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Dan Radez <dradez@redhat.com> - 3.1.0-1
- updating to 3.1.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.1-2
- Rebuilt for Python 3.9

* Fri May 08 2020 Dan Radez <dradez@redhat.com> - 3.0.1-1
- updating to 3.0.1-1
- added toml dep

* Wed Feb 12 2020 Dan Radez <dradez@redhat.com> - 3.0.0-1
- updating to 3.0.0-1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 27 2019 Dan Radez <dradez@redhat.com> - 2.0-4
- Rebuilding to resolve dep issues

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 03 2019 Dan Radez <dradez@redhat.com> - 2.0-1
- Initial package.
