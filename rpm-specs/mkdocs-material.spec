%global forgeurl https://github.com/squidfunk/mkdocs-material

Name:           mkdocs-material
Version:        9.5.33
Release:        1%{?dist}
Summary:        Material design theme for MkDocs

License:        MIT
URL:            https://squidfunk.github.io/mkdocs-material
Source:         %{forgeurl}/archive/%{version}/%{name}-%{version}.tar.gz
# Drop mkdocs-material-extensions from requirements
Patch:          %{forgeurl}/pull/7486.patch

BuildArch:      noarch
BuildRequires:  python3-devel

%description
This package provides a powerful documentation framework on top of MkDocs.

%prep
%autosetup -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files material

%check
export PYTHONPATH="%{buildroot}/%{python3_sitelib}"
mkdocs new testing
pushd testing
mkdocs build --theme material
popd

%files -f %{pyproject_files}
%doc README.md

%changelog
* Wed Aug 28 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 9.5.33-1
- Update to 9.5.33; Fixes: RHBZ#2308408
- Convert to pyproject macros

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 5.0.2-6
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Robin Lee <cheeselee@fedoraproject.org> - 5.0.2-3
- BR python3dist(setuptools)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.0.2-2
- Rebuilt for Python 3.9

* Sat Apr 11 2020 Robin Lee <cheeselee@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2

* Wed Apr  8 2020 Robin Lee <cheeselee@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1
- No globbing %%{python3_sitelib}

* Sun Mar  8 2020 Robin Lee <cheeselee@fedoraproject.org> - 4.6.3-1
- Update to 4.6.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-7
- Rebuilt for Python 3.7

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 07 2016 William Moreno <williamjmorenor@gmail.com> - 0.2.2-1
- Update to v.0.2.2
- Fix license tag.

* Fri Feb 12 2016 William Moreno <williamjmorenor@gmail.com> - 0.1.1-1
- Initial Packaging
