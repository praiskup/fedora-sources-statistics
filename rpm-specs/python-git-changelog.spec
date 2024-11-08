Name:           python-git-changelog
Version:        2.5.2
Release:        %autorelease
Summary:        Automatic Changelog generator using Jinja2 templates
License:        ISC
URL:            https://github.com/pawamoy/git-changelog
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  git-core

%global _description %{expand:
Automatic Changelog generator using Jinja2 templates
From git logs to change logs
This is a general software development utility.}

%description %_description

%package -n python3-git-changelog
Requires:       git-core
Summary:        %{summary}

%description -n python3-git-changelog %_description

%prep
%autosetup -n git-changelog-%{version} -S git
sed -i 's/^Jinja2.*/Jinja2 = "*"/' pyproject.toml
git tag %{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files git_changelog
rm -fv %{buildroot}%{python3_sitelib}/README.md
rm -fv %{buildroot}%{python3_sitelib}/pyproject.toml

%check
%pytest

%files -n python3-git-changelog -f %{pyproject_files}
%doc README.* CHANGELOG.* CODE_OF_CONDUCT.* CONTRIBUTING.*
%license LICENSE*
%{_bindir}/git-changelog

%changelog
%autochangelog
