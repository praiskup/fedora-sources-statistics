Name:           python-inline-snapshot
Version:        0.13.3
Release:        %autorelease
Summary:        Golden master/snapshot/approval testing library

# SPDX
License:        MIT
URL:            https://github.com/15r10nk/inline-snapshot
Source:         %{pypi_source inline_snapshot}

BuildArch:      noarch

BuildRequires:  python3-devel

# For extracting test dependencies from pyproject.toml:
BuildRequires:  tomcli

# Extra test dependencies:
# For test_xdist, test_xdist_disabled, test_xdist_and_disable
BuildRequires:  %{py3_dist pytest-xdist}

%global common_description %{expand:
Golden master/snapshot/approval testing library which puts the values right
into your source code.}

%description %{common_description}


%package -n python3-inline-snapshot
Summary:        %{summary}

%description -n python3-inline-snapshot %{common_description}


%prep
%autosetup -n inline_snapshot-%{version} -p1
# Extract test dependencies from pyproject.toml; filter out those that are not
# needed (currently, typecheckers; see
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters).
tomcli get pyproject.toml -F newline-list \
    'tool.hatch.envs.hatch-test.extra-dependencies' |
    grep -vE '^(pyright|mypy)' |
    tee _test-requirements.txt


%generate_buildrequires
%pyproject_buildrequires _test-requirements.txt


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l inline_snapshot


%check
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
ignore="${ignore-} --ignore=tests/test_typing.py"

%pytest ${ignore-} -v


%files -n python3-inline-snapshot -f %{pyproject_files}


%changelog
%autochangelog
