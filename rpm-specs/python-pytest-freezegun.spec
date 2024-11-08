Name:           python-pytest-freezegun
Version:        0.4.2
Release:        %autorelease
Summary:        Wrap pytest tests with fixtures in freeze_time

License:        MIT
URL:            https://github.com/ktosiek/pytest-freezegun
Source0:        %{url}/archive/%{version}/pytest-freezegun-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel

%global _description %{expand:
This is a pytest plugin that let you wrap tests with fixtures in freeze_time.

Features:

- Freeze time in both the test and fixtures
- Access the freezer when you need it}

%description %_description


%package -n python3-pytest-freezegun
Summary:        %{summary}

%description -n python3-pytest-freezegun %_description


%prep
%autosetup -p1 -n pytest-freezegun-%{version}


%generate_buildrequires
# tox config contains coverage, so we'll execute pytest directly instead
# since this a pytest plugin, pytetst is a runtime dependency anyway
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files pytest_freezegun


%check
%pytest -v


%files -n python3-pytest-freezegun -f %{pyproject_files}
%doc README.rst CHANGELOG.md
%license LICENSE


%changelog
%autochangelog
