%global pypi_name myst-parser

Name:           python-%{pypi_name}
Version:        4.0.0
Release:        %autorelease
Summary:        A commonmark compliant parser, with bridges to docutils & sphinx

# SPDX
License:        MIT
URL:            https://github.com/executablebooks/MyST-Parser
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

# Fix the expected test output
Patch:          https://github.com/executablebooks/MyST-Parser/pull/973.patch

BuildArch:      noarch

BuildRequires:  python3-devel

# Test dependencies- upstream uses tox with complicated matrix
# mixed with coverage, it's easier to set the ones we want here
BuildRequires:  python3-pytest
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-docutils
BuildRequires:  python3-pytest-regressions
BuildRequires:  python3-pytest-param-files
BuildRequires:  python3-sphinx-pytest
BuildRequires:  python3-linkify-it-py


%global _description %{expand:
A fully-functional markdown flavor and parser for Sphinx.
MyST allows you to write Sphinx documentation entirely in markdown.
MyST markdown provides a markdown equivalent of the reStructuredText syntax,
meaning that you can do anything in MyST that you can do with reStructuredText.
It is an attempt to have the best of both worlds: the flexibility and
extensibility of Sphinx with the simplicity and readability of Markdown.
}

%description %_description


%package -n     python3-%{pypi_name}
Summary:        %{summary}


%description -n python3-%{pypi_name} %_description

%prep
%autosetup -p1 -n MyST-Parser-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files myst_parser

%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/myst-anchors
%{_bindir}/myst-docutils-demo
%{_bindir}/myst-docutils-html
%{_bindir}/myst-docutils-html5
%{_bindir}/myst-docutils-latex
%{_bindir}/myst-docutils-xml
%{_bindir}/myst-docutils-pseudoxml
%{_bindir}/myst-inv

%changelog
%autochangelog
