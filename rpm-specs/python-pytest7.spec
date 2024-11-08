Name:           python-pytest7
%global base_version 7.4.3
#global prerelease ...
Version:        %{base_version}%{?prerelease:~%{prerelease}}
Release:        %autorelease
Summary:        pytest 7.x for compatibility purposes
License:        MIT
URL:            https://pytest.org
Source:         %{pypi_source pytest %{base_version}%{?prerelease}}
# see https://github.com/pytest-dev/pytest/issues/10042#issuecomment-1237132867
Patch:          pytest-7.1.3-fix-xfails.patch
# XFAIL TestLocalPath.test_make_numbered_dir_multiprocess_safe
Patch:          https://github.com/pytest-dev/pytest/pull/11611.patch

# Remove -s from Python shebang,
# ensure that packages installed with pip to user locations are testable
# https://bugzilla.redhat.com/2152171
%undefine _py3_shebang_s

# When building pytest for the first time with new Python version
# we might not yet have all the BRs, those conditionals allow us to do that.

# This can be used to disable all tests for faster bootstrapping.
# The tests are enabled by default except when building on RHEL/ELN
# (to avoid pulling in extra dependencies into next RHEL).
%bcond tests %{undefined rhel}

# Only disabling the optional tests is a more complex but careful approach
# Pytest will skip the related tests, so we only conditionalize the BRs
%bcond optional_tests %{with tests}

# To run the tests in %%check we use pytest-timeout
# When building pytest for the first time with new Python version
# that is not possible as it depends on pytest
%bcond timeout %{with tests}

# When building pytest for the first time with new Python version
# we also don't have sphinx yet and cannot build docs.
# The docs are enabled by default except when building on RHEL/ELN
# (to avoid pulling in extra dependencies into next RHEL).
%bcond docs %{undefined rhel}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros >= 0-51

%if %{with tests}
# we avoid using %%pyproject_buildrequires -x testing as it mixes optional and non-optional deps
BuildRequires:  python3-attrs >= 19.2
BuildRequires:  python3-hypothesis >= 3.56
BuildRequires:  python3-pygments >= 2.7.2
BuildRequires:  python3-xmlschema
%if %{with optional_tests}
BuildRequires:  python3-argcomplete
#BuildRequires:  python3-asynctest -- not packaged in Fedora
BuildRequires:  python3-decorator
BuildRequires:  python3-jinja2
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-numpy
BuildRequires:  python3-pexpect
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-twisted
BuildRequires:  /usr/bin/lsof
%endif
%if %{with timeout}
BuildRequires:  python3-pytest-timeout
%endif
%endif

%if %{with docs}
BuildRequires:  %{_bindir}/rst2html
BuildRequires:  python3-pygments-pytest
BuildRequires:  python3-Pallets-Sphinx-Themes
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-removed-in
BuildRequires:  python3-sphinxcontrib-trio
# See doc/en/conf.py -- sphinxcontrib.inkscapeconverter is only used when inkscape is available
# we don't BR inkscape so we generally don't need it, but in case inkscape is installed accidentally:
BuildRequires:  (python3-sphinxcontrib-inkscapeconverter if inkscape)
BuildRequires:  make
%endif

BuildArch:      noarch

%description
The pytest framework makes it easy to write small tests, yet scales to support
complex functional testing for applications and libraries.

This package contains pytest 7.x for compatibility reasons.
Use pytest 8 if at all possible.


%package -n python3-pytest7
Summary:        Simple powerful testing with Python
Provides:       pytest = %{version}-%{release}
%py_provides    python3-pytest
Conflicts:      python3-pytest
Provides:       deprecated()

%description -n python3-pytest7
The pytest framework makes it easy to write small tests, yet scales to support
complex functional testing for applications and libraries.

This package contains pytest 7.x for compatibility reasons.
Use pytest 8 if at all possible.


%prep
%autosetup -p1 -n pytest-%{base_version}%{?prerelease}

# Between 7.2.0 and 7.2.1 the tests were updated for pygments 2.14.
# See https://github.com/pytest-dev/pytest/pull/10632 + 10637 (backport to 7.2).
# To make the tests work with pygments 2.13, we set the added {endline}s to empty.
# Once pygments 2.14+ is omnipresent, feel free to remove this hack,
# but bump the minimal BuildRequired version of python3-pygments to 2.14.
%if v"0%(%{python3} -c "import pygments; print(pygments.__version__)" 2>/dev/null)" < v"2.14~~"
sed -i 's/"endline": "\\x1b\[90m\\x1b\[39;49;00m",/"endline": "",/' testing/conftest.py
%endif

# pytest 7 needs pluggy < 1.4 to work properly
sed -i "s/pluggy>=0.12,<2.0/pluggy>=0.12,<1.4/" setup.cfg


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel

%if %{with docs}
for l in doc/* ; do
  %make_build -C $l html PYTHONPATH="$(pwd)/src"
done
for f in README CHANGELOG CONTRIBUTING ; do
  rst2html ${f}.rst > ${f}.html
done
%endif


%install
%pyproject_install
%pyproject_save_files _pytest pytest py

mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-%{python3_version}
ln -snf pytest-%{python3_version} %{buildroot}%{_bindir}/pytest-3
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-%{python3_version}
ln -snf py.test-%{python3_version} %{buildroot}%{_bindir}/py.test-3

# We use 3.X per default
ln -snf pytest-%{python3_version} %{buildroot}%{_bindir}/pytest
ln -snf py.test-%{python3_version} %{buildroot}%{_bindir}/py.test

%if %{with docs}
mkdir -p _htmldocs/html
for l in doc/* ; do
  # remove hidden file
  rm ${l}/_build/html/.buildinfo
  mv ${l}/_build/html _htmldocs/html/${l##doc/}
done
%endif

# remove shebangs from all scripts
find %{buildroot}%{python3_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;


%check
%if %{with tests}
%global __pytest %{buildroot}%{_bindir}/pytest
# optional_tests deps contain pytest-xdist, so we can use it to run tests faster
# some tests are failing with python 3.13, since this is a temporary compat
# package we have decided to skip them
%pytest testing %{?with_timeout:--timeout=30} %{?with_optional_tests:-n auto} -rs \
    -k "not test_get_user_uid_not_found and not test_traceback_recursion_index and \
    not test_pdb_used_outside_test and not test_pdb_used_in_generate_tests and \
    not test_getfuncargnames_partial and not test_excinfo_no_sourcecode and \
    not test_repr_traceback_recursion and not test_getfslineno and \
    not test_exception_repr_extraction_error_on_recursion and \
    not test_collect_protocol_single_function and \
    not test_collect_custom_nodes_multi_id and \
    not test_collect_subdir_event_ordering and \
    not test_collect_two_commandline_args and \
    not test_doctest_unexpected_exception and \
    not test_doctest_linedata_on_property and \
    not test_tmp_path_fallback_uid_not_found"
%else
%pyproject_check_import
%endif


%files -n python3-pytest7 -f %{pyproject_files}
%if %{with docs}
%doc CHANGELOG.html
%doc README.html
%doc CONTRIBUTING.html
%doc _htmldocs/html
%endif
%{_bindir}/pytest
%{_bindir}/pytest-3
%{_bindir}/pytest-%{python3_version}
%{_bindir}/py.test
%{_bindir}/py.test-3
%{_bindir}/py.test-%{python3_version}


%changelog
%autochangelog
