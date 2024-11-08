# tests are enabled by default
%bcond_without tests

Name:           python-six
Version:        1.16.0
Release:        %autorelease
Summary:        Python 2 and 3 compatibility utilities

# SPDX
License:        MIT
URL:            https://github.com/benjaminp/six
Source0:        %{pypi_source six}

# tkinter.tix was removed from Python 3.13, skip the test
# https://github.com/benjaminp/six/pull/377
Patch:          tkinter.tix-was-removed-from-Python-3.13.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-tkinter
%endif

%global _description %{expand:
Six is a Python 2 and 3 compatibility library. It provides utility functions
for smoothing over the differences between the Python versions with the goal
of writing Python code that is compatible on both Python versions.}

%description %{_description}


%package -n python%{python3_pkgversion}-six
Summary:        %{summary}

%description -n python%{python3_pkgversion}-six %{_description}


%prep
%autosetup -p1 -n six-%{version}


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files six


%if %{with tests}
%check
%pytest
%endif


%files -n python%{python3_pkgversion}-six -f %{pyproject_files}
%license LICENSE
%doc README.rst documentation/index.rst


%changelog
%autochangelog
