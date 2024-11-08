%global pypi_name pymdown-extensions

Name:           python-%{pypi_name}
Version:        10.9
Release:        1%{?dist}
Summary:        Extension pack for Python Markdown

# Most of the package is MIT except two files (highlight.py and superfences.py)
License:        MIT and BSD-2-Clause
URL:            https://facelessuser.github.io/pymdown-extensions
Source:         %{pypi_source pymdown_extensions}

BuildArch:      noarch
 
%description
PyMdown Extensions (pymdownx) is a collection of extensions for Python
Markdown.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
# Needed for the tests to pass
BuildRequires:  python3-pygments >= 2.18.0

%description -n python3-%{pypi_name}
PyMdown Extensions (pymdownx) is a collection of extensions for Python
Markdown.

%pyproject_extras_subpkg -n python3-pymdown-extensions extra

%prep
%autosetup -n pymdown_extensions-%{version} -p1

# Drop invalid entry that breaks the pyproject macros
sed -i '/\.\[extra\]/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -t -x extra

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pymdownx

%check
%tox

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 28 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 10.9-1
- Update to 10.9; Fixes: RHBZ#2308406
- Convert to pyproject macros
- Convert license tag to SPDX

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 7.0-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 7.0-2
- Rebuilt for Python 3.9

* Wed Apr  8 2020 Robin Lee <cheeselee@fedoraproject.org> - 7.0-1
- Update to 7.0

* Thu Mar 12 2020 Robin Lee <cheeselee@fedoraproject.org> - 6.3-2
- Bump release for koji error:
  https://pagure.io/fedora-infrastructure/issue/8738

* Sun Mar  8 2020 Robin Lee <cheeselee@fedoraproject.org> - 6.3-1
- Update to 6.3

* Wed Apr 11 2018 Stephen Gallagher <sgallagh@redhat.com> - 3.5-4
- Update license information

* Wed Apr 04 2018 Stephen Gallagher <sgallagh@redhat.com> - 3.5-1
- Initial package.
