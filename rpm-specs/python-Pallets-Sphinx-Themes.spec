%global pypi_name Pallets-Sphinx-Themes

Name:           python-%{pypi_name}
Version:        2.1.3
Release:        3%{?dist}
Summary:        Sphinx themes for Pallets and related projects

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/pallets/pallets-sphinx-themes/
Source0:        %{pypi_source pallets_sphinx_themes}
BuildArch:      noarch

BuildRequires:  python3-devel

%description
Pallets Sphinx Themes Themes for the Pallets projects.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

Requires:       python3-sphinx
%description -n python3-%{pypi_name}
Pallets Sphinx Themes Themes for the Pallets projects.


%prep
%autosetup -n pallets_sphinx_themes-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pallets_sphinx_themes

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE.txt
%doc README.md CHANGES.rst

%changelog
* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.1.3-3
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Karolina Surma <ksurma@redhat.com> - 2.1.3-1
- Update to 2.1.3

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.1.1-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.2-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.2-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.2.2-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.2-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Rick Elrod <relrod@redhat.com> - 1.2.2-3
- Fix dependency issue for python >=3.8

* Mon Nov 4 2019 Rick Elrod <relrod@redhat.com> - 1.2.2-2
- Fix files section for python >=3.10

* Mon Nov 4 2019 Rick Elrod <relrod@redhat.com> - 1.2.2-1
- Latest upstream
- Remove python 2 stuff, to follow Fedora packaging guidelines

* Sat Apr 28 2018 Rick Elrod <rick@elrod.me> - 1.0.0-1
- Initial package.
