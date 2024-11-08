Name:           python-py-tes
Version:        0.4.2
Release:        %autorelease
Summary:        Python SDK for the GA4GH Task Execution API

# SPDX
License:        MIT
URL:            https://github.com/ohsu-comp-bio/py-tes
# The PyPI sdist is missing the LICENSE and the tests, so we must use the
# GitHub source archive.
Source:         %{url}/archive/%{version}/py-tes-%{version}.tar.gz

# Remove unused future dependency
# https://github.com/ohsu-comp-bio/py-tes/pull/61
#   Fixes:
# [HEADS UP] python-py-tes buildrequires python3-future which won't work with
# Python 3.13 (Fedora 41+)
# https://bugzilla.redhat.com/show_bug.cgi?id=2276617
Patch:          %{url}/pull/61.patch

BuildArch:      noarch

BuildRequires:  python3-devel

# Most of the dependencies in tests/requirements.txt pertain to linting and
# coverage analysis. (Plus, the package wants to use the deprecated nose
# package as the test runner.) Rather than working around all of these, it is
# simpler to BR and invoke pytest manually.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist requests_mock} >= 1.3

%global common_description %{expand:
This is a library for interacting with servers implementing the GA4GH Task
Execution Schema (https://github.com/ga4gh/task-execution-schemas).}

%description %{common_description}


%package -n python3-py-tes
Summary:        %{summary}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-tes

%description -n python3-py-tes %{common_description}


%prep
%autosetup -n py-tes-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l tes


%check
%pytest -v


%files -n python3-py-tes -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
