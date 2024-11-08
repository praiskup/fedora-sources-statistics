%global _description %{expand:
webcolors is a module for working with HTML/CSS color definitions.

Support is included for normalizing and converting between the following
formats (RGB colorspace only; conversion to/from HSL can be handled by the
colorsys module in the Python standard library):
* Specification-defined color names
* Six-digit hexadecimal
* Three-digit hexadecimal
* Integer rgb() triplet
* Percentage rgb() triplet}

Name:           python-webcolors
Version:        1.13
Release:        7%{?dist}
Summary:        A library for working with HTML and CSS color names and value formats

License:        BSD-3-Clause
URL:            https://github.com/ubernostrum/webcolors
Source:         %{pypi_source webcolors}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest


%description %_description


%package -n python3-webcolors
Summary:        %{summary}


%description -n python3-webcolors %_description


%prep
%autosetup -n webcolors-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files webcolors


%check
%pytest -v


%files -n python3-webcolors -f %{pyproject_files}
%doc README.rst


%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.13-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.13-2
- Rebuilt for Python 3.12

* Sat Apr 08 2023 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.13-1
- Bumped version to 1.13

* Wed Feb 15 2023 Carl George <carl@george.computer> - 1.12-4
- Convert to pyproject macros

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.12-1
- Bumped version to 1.12

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.11.1-8
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.11.1-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.11.1-2
- Rebuilt for Python 3.9

* Tue Feb 18 2020 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.11.1-1
- Bumped version to 1.11.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.10-1
- Bumped version to 1.10

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.9.1-1
- Bumped version to 1.9.1

* Sun Jun 02 2019 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.9-1
- Bumped version to 1.9

* Tue Feb 05 2019 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.7-9
- Catch up with packaging guidelines
- In general, use recommended RPM macros
- Drop the Python 2 package
- Inline package description

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 10 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7-4
- Python 2 binary package renamed to python2-webcolors
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.7-2
- Python 3 detection for epel7

* Fri Feb 10 2017 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.7-1
- Bumped version to 1.7
- Updated URL

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.5-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 24 2016 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.5-1
- Bumped version to 1.5
- Upstream now ships tests and documentation

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Dec 09 2013 Dridi Boukelmoune <dridi@fedoraproject.org> - 1.4-1
- Initial spec
