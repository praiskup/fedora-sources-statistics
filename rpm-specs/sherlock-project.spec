# Packager: Paul Pfeister <code@pfeister.dev> (GitHub @ppfeister)
Name:           sherlock-project
Version:        0.15.0
Release:        %autorelease
Summary:        Hunt down social media accounts by username across social networks

License:        MIT
URL:            https://github.com/sherlock-project/sherlock
Source:         %{url}/archive/v%{version}/sherlock-%{version}.tar.gz

Patch0:         0001-Remove-tor.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  help2man

%global _description %{expand:
Hunt down social media accounts by username across 400+ social networks and
websites. New targets are tested and implemented regularly.
}

%description %{_description}


%prep
%autosetup -p1 -n sherlock-%{version}
sed -i '/torrequest/d' 'pyproject.toml' # Pending upstream removal

%generate_buildrequires
%pyproject_buildrequires -t -x dev


%build
# Project now uses Poetry and dynamic versioning, so pyproject version is 0
# __init__ is currently the single source of truth for version info
sherlock_version=$(sed -n 's/^__version__ *= *"\([0-9.]*\)"/\1/p' sherlock_project/__init__.py)
sed -r -i "s/^version *= .*?$/version = \"$sherlock_version\"/" pyproject.toml
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -L sherlock_project

sed -r -i '1{/^#!/d}' '%{buildroot}%{python3_sitelib}/sherlock_project/__main__.py'
sed -r -i '1{/^#!/d}' '%{buildroot}%{python3_sitelib}/sherlock_project/sherlock.py'

install -d '%{buildroot}%{_mandir}/man1'
PYTHONPATH='%{buildroot}%{python3_sitelib}' help2man \
    --no-info \
    --version-string='%{version}' \
    --name='%{summary}' \
    --output='%{buildroot}%{_mandir}/man1/sherlock.1' \
    '%{buildroot}%{_bindir}/sherlock'


%check
%tox -e offline


%files -f %{pyproject_files}
%license LICENSE
%doc docs/README.md
%{_bindir}/sherlock
%{_mandir}/man1/sherlock.1*


%changelog
* Mon Jul 08 2024 Paul Pfeister <code@pfeister.dev> - 0.15.0-1
- Importable module renamed to sherlock_project (see Debian 1072733).
- --dump-response flag added to aid in debugging.
* Tue May 14 2024 Paul Pfeister <code@pfeister.dev> - 0.14.4-1
- Initial package.
