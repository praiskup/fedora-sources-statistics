%global modname flask
%global srcname flask

Name:           python-%{modname}
Version:        3.0.3
Release:        %autorelease
Epoch:          1
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions

License:        BSD-3-Clause
URL:            http://flask.pocoo.org/
Source0:        %{pypi_source}

BuildArch:      noarch

%global _description \
Flask is called a “micro-framework” because the idea to keep the core\
simple but extensible. There is no database abstraction layer, no form\
validation or anything else where different libraries already exist\
that can handle that. However Flask knows the concept of extensions\
that can add this functionality into your application as if it was\
implemented in Flask itself. There are currently extensions for object\
relational mappers, form validation, upload handling, various open\
authentication technologies and more.

%description %{_description}

%package -n python3-%{modname}
Summary:        %{summary}
BuildRequires:  make
BuildRequires:  python3-devel

%description -n python3-%{modname} %{_description}

Python 3 version.

%package doc
Summary:        Documentation for %{name}

%description doc
Documentation and examples for %{name}.

%pyproject_extras_subpkg -n python3-%{modname} async
%generate_buildrequires
# -t picks test.txt by default which contains too tight pins
%pyproject_buildrequires -x async requirements/tests.in requirements/docs.in

%prep
%autosetup -n %{srcname}-%{version}
rm -rf examples/flaskr/
rm -rf examples/minitwit/

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{modname}

mv %{buildroot}%{_bindir}/%{modname}{,-%{python3_version}}
ln -s %{modname}-%{python3_version} %{buildroot}%{_bindir}/%{modname}-3
ln -sf %{modname}-3 %{buildroot}%{_bindir}/%{modname}

pushd docs
# PYTHONPATH to prevent "'Flask' must be installed to build the documentation."
make PYTHONPATH=%{buildroot}/%{python3_sitelib} SPHINXBUILD=sphinx-build-3 html
rm -v _build/html/.buildinfo
popd

%check
%pytest -Wdefault

%files -n python3-%{modname} -f %{pyproject_files}
%license LICENSE.txt
%doc CHANGES.rst README.md
%{_bindir}/%{modname}
%{_bindir}/%{modname}-3
%{_bindir}/%{modname}-%{python3_version}

%files doc
%license LICENSE.txt
%doc docs/_build/html examples

%changelog
%autochangelog
