# We cannot build the documentation due to missing dependencies:
# myst-nb, sphinx-book-theme
%bcond doc 0

# python-jupytext cannot be built for s390x at present
# python-nbdime can only be built for x86_64 and aarch64 at present
%ifarch x86_64 aarch64
%bcond test 1
%else
%bcond test 0
%endif

%global giturl  https://github.com/executablebooks/jupyter-cache

Name:           python-jupyter-cache
Version:        1.0.0
Release:        %autorelease
Summary:        Manage a cache of Jupyter notebooks

License:        MIT
BuildArch:      noarch
URL:            https://jupyter-cache.readthedocs.io/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/v%{version}/jupyter-cache-%{version}.tar.gz

BuildRequires:  help2man
BuildRequires:  python3-devel

%if %{with doc}
BuildRequires:  make
BuildRequires:  python3-docs
%endif

%global _desc %{expand:
This package provides a defined interface for working with a cache of
Jupyter notebooks.  It is useful if you have a number of notebooks whose
execution outputs you want to ensure are kept up to date, without having
to re-execute them every time (particularly for long running code, or
text-based formats that do not store the outputs).

The notebooks must have deterministic execution outputs:

- You use the same environment to run them (e.g. the same installed
  packages)
- They run no nondeterministic code (e.g. random numbers)
- They do not depend on external resources (e.g. files or network
  connections) that change over time}

%description %_desc

%package     -n python3-jupyter-cache
Summary:        %{summary}
Recommends:     %{py3_dist jupytext}
Recommends:     %{py3_dist nbdime}

%description -n python3-jupyter-cache %_desc

%if %{with doc}
%package        doc
Summary:        Documentation for %{name}

%description    doc
Documentation for %{name}.
%endif

%pyproject_extras_subpkg -n python3-jupyter-cache cli

%prep
%autosetup -n jupyter-cache-%{version}

# Use local objects.inv for intersphinx
sed -e 's|\("https://docs\.python\.org/[.[:digit:]]*", \)None|\1"%{_docdir}/python3-docs/html/objects.inv"|' \
    -i docs/conf.py

%generate_buildrequires
%pyproject_buildrequires -x cli%{?with_doc:,rtd}%{?with_test:,testing -t}

%build
%pyproject_wheel

%if %{with doc}
# Build the documentation
PYTHONPATH=$PWD make -C docs html
rm docs/_build/html/.buildinfo
%endif

%install
%pyproject_install
%pyproject_save_files -L jupyter_cache

export PYTHONPATH=%{buildroot}%{python3_sitelib}
mkdir -p %{buildroot}%{_mandir}/man1
help2man -N --version-string=%{version} \
  -n 'Manage a cache of Jupyter notebooks' \
  -o %{buildroot}%{_mandir}/man1/jcache.1 %{buildroot}%{_bindir}/jcache

%if %{with test}
%check
%tox
%endif

%files -n python3-jupyter-cache -f %{pyproject_files}
%doc CHANGELOG.md README.md
%license LICENSE
%{_bindir}/jcache
%{_mandir}/man1/jcache.1*

%if %{with doc}
%files doc
%doc doc/_build/html
%license LICENSE
%endif

%changelog
%autochangelog
