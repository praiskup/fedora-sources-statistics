Name:           python-cfgv
Version:        3.4.0
Release:        %autorelease
Summary:        Validate configuration and produce human readable error messages

# SPDX
License:        MIT
URL:            https://github.com/asottile/cfgv
Source:         %{url}/archive/v%{version}/cfgv-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

%global common_description %{expand:
%{summary}.}

%description %{common_description}


%package -n     python3-cfgv
Summary:        %{summary}

%description -n python3-cfgv %{common_description}


%prep
%autosetup -n cfgv-%{version}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -r -i 's/^(cov|flake8)/# &/' requirements-dev.txt


%generate_buildrequires
%pyproject_buildrequires requirements-dev.txt


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l cfgv


%check
%pytest


%files -n python3-cfgv -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
