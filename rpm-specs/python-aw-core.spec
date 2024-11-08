%global srcname aw-core
%global commit 3b83ab542406349b3d5e601318289b77d23d906f
%global short_commit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{srcname}
Version:        0.5.16^20240507.%{short_commit}
Release:        %autorelease
Summary:        Core library for ActivityWatch

License:        MPL-2.0
URL:            https://github.com/ActivityWatch/aw-core
Source:         %{url}/archive/%{commit}/%{srcname}-%{short_commit}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  help2man
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Core library for ActivityWatch.}

%description %{_description}

%package -n python3-%{srcname}
Summary:    %{summary}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{commit}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -ri '/^[[:blank:]]*pytest-cov\b/d' pyproject.toml
sed -ri '/^[[:blank:]]*pylint\b/d' pyproject.toml
sed -ri '/^[[:blank:]]*black\b/d' pyproject.toml

# works also with 3.9 on f39 and 3.11 on f40, so unpinning
sed -ri 's/platformdirs = "3.10"/platformdirs = ">=3.9"/' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files {aw_core,aw_datastore,aw_transform,aw_query}
install -Dm 0644 %{_builddir}/%{srcname}-%{commit}/aw_cli/* -t %{buildroot}%{python3_sitelib}/aw_cli
mkdir -p %{buildroot}%{_mandir}/man1
help2man --no-discard-stderr %{buildroot}%{_bindir}/aw-cli -o %{buildroot}%{_mandir}/man1/aw-cli.1

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license LICENSE.txt
%{_mandir}/man1/aw-cli.1*
%{_bindir}/aw-cli
%{python3_sitelib}/aw_cli

%changelog
%autochangelog
