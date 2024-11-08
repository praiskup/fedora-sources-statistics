# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond doc 1

Name:           python-nose2
Version:        0.15.1
Release:        %autorelease
Summary:        The successor to nose, based on unittest2

# The entire source is BSD-2-Clause, except that unspecified portions are
# derived from unittest2 under a BSD-3-Clause. See LICENSE.
License:        BSD-2-Clause AND BSD-3-Clause
URL:            https://nose2.io/
%global forgeurl https://github.com/nose-devs/nose2
Source0:        %{forgeurl}/archive/%{version}/nose2-%{version}.tar.gz
# Man page written for Fedora in groff_man(7) format based on --help output
Source1:        nose2.1

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  tomcli

%if %{with doc}
BuildRequires:  make
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
%endif

%global common_description %{expand:
nose2 is the successor to nose.

It’s unittest with plugins.

nose2’s purpose is to extend unittest to make testing nicer and easier to
understand.}

%description %{common_description}


%package -n python3-nose2
Summary:        Next generation of nicer testing for Python

%description -n python3-nose2 %{common_description}


%if %{with doc}
%package        doc
Summary:        Documentation for %{name}

%description    doc %{common_description}
%endif


%pyproject_extras_subpkg -n python3-nose2 coverage_plugin


%prep
%autosetup -n nose2-%{version} -p1

# Patch out unnecessary documentation dependency on sphinx-issues, used
# upstream for changelog generation.
sed -r -i '/"sphinx_issues",/d' docs/conf.py
tomcli set pyproject.toml lists delitem project.optional-dependencies.dev \
    'sphinx-issues*'
# Since we are not building HTML documentation, we do not need the HTML theme
# either.
tomcli set pyproject.toml lists delitem project.optional-dependencies.dev \
    'sphinx-rtd-theme*'
%if %{without doc}
tomcli set pyproject.toml lists delitem project.optional-dependencies.dev \
    'sphinx*'
%endif

# Workaround for https://github.com/rpm-software-management/rpm/issues/2532:
rm -rf SPECPARTS

# Remove shebangs from non-script sources. The find-then-modify pattern
# preserves mtimes on sources that did not need to be modified.
find nose2/ -type f -name '*.py' \
    -exec gawk '/^#!/ { print FILENAME }; { nextfile }' '{}' '+' |
  xargs -r -t sed -r -i '1{/^#!/d}'


%generate_buildrequires
%pyproject_buildrequires -e %{toxenv}-nocov


%build
%pyproject_wheel
%if %{with doc}
PYTHONPATH="${PWD}" %make_build -C docs latex \
    SPHINXOPTS='-j%{?_smp_build_ncpus}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif


%install
%pyproject_install
%pyproject_save_files -l nose2

# Don’t install the tests; we are not sure how to fix this *successfully* in
# pyproject.toml, even after reading
# https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#setuptools-specific-configuration,
# so we haven’t suggested any change upstream. Still, the tests are large and
# unlikely to be useful to package users.
rm -rvf '%{buildroot}%{python3_sitelib}/nose2/tests/'
sed -r -i '/\/nose2\/tests(\/|$)/d' %{pyproject_files}

install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 '%{SOURCE1}'


%check
%tox -e %{default_toxenv}-nocov


%files -n python3-nose2 -f %{pyproject_files}
%doc AUTHORS
%if %{without doc}
%doc README.rst docs/changelog.rst
%endif

%{_bindir}/nose2
%{_mandir}/man1/nose2.1*


%if %{with doc}
%files doc
%license LICENSE
%doc AUTHORS README.rst docs/changelog.rst

%doc docs/_build/latex/nose2.pdf
%endif


%changelog
%autochangelog
