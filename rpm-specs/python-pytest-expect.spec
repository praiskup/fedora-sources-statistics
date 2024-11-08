%global pypi_name pytest-expect

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        %autorelease
Summary:        py.test plugin to store test expectations and mark tests based on them

License:        MIT
URL:            https://github.com/gsnedders/pytest-expect
Source0:        %pypi_source
Source1:        %{url}/raw/%{version}/LICENSE

# Explicitly require six, it is imported but was not required.
# In the past, it might have been transitively pulled in by pytest.
Patch:          %{url}/pull/16.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%description
A py.test plugin that stores test expectations by saving the set of failing
tests, allowing them to be marked as xfail when running them in future.
The tests expectations are stored such that they can be distributed alongside
the tests.


%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
A py.test plugin that stores test expectations by saving the set of failing
tests, allowing them to be marked as xfail when running them in future.
The tests expectations are stored such that they can be distributed alongside
the tests.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}
cp -p %{SOURCE1} .

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files pytest_expect


%check
%pyproject_check_import


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
