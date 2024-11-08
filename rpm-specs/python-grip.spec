%global pypi_name grip

Name:           python-%{pypi_name}
Version:        4.6.2
Release:        %{autorelease}
Summary:        Render local readme files before sending off to GitHub

%global forgeurl https://github.com/joeyespo/grip
# Version 4.6.2 has not been tagged in git. Use commit.
%global commit ed3adea5a2f32af8062a97917e26a61dfe9fb589
%global distprefix %{nil}
%forgemeta

License:        MIT
URL:            %forgeurl
Source:         %forgesource
# Remove use of vendored `six` (downstream only patch)
Patch:          unvendor_six.patch

BuildArch:      noarch
BuildRequires:  help2man
BuildRequires:  python3-devel

%global _description %{expand:
Grip is a command-line server application written in Python that uses
the GitHub markdown API to render a local readme file. The styles and
rendering come directly from GitHub, so you'll know exactly how it will
appear. Changes you make to the Readme will be instantly reflected in
the browser without requiring a page refresh.}

%description %_description


%package -n python3-%{pypi_name}
Summary:        %{summary}
# Package bundles fonts and icons from GitHub Octicons (MIT)
# https://github.com/primer/octicons
# Bundled version according to release date just before the commit.
Provides:       bundled(octicons-fonts) = 4.3.0

%description -n python3-%{pypi_name} %_description


%prep
%forgeautosetup -p1

# Remove linter from test requirements
sed -r \
    -e '/flake8/d' \
    -i requirements-test.txt

# Use system installed `six` instead of vendored module
rm -rf grip/vendor/six.py
echo "six" >> requirements.txt


%generate_buildrequires
%pyproject_buildrequires -x tests


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

mkdir -p %{buildroot}%{_mandir}/man1
%{py3_test_envvars} \
  help2man --no-info \
  -o %{buildroot}%{_mandir}/man1/%{pypi_name}.1 --no-discard-stderr \
  %{buildroot}%{_bindir}/%{pypi_name}


%check
# `test_github.py` requires network - exclude it
%pytest -v --ignore tests/test_github.py
# Run import test in addition to unit tests
%pyproject_check_import


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc CHANGES.md README.md
%{_bindir}/%{pypi_name}
%{_mandir}/man1/%{pypi_name}.1*

%changelog
%autochangelog
