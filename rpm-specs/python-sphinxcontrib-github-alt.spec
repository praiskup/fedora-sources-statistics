Name:           python-sphinxcontrib-github-alt
Version:        1.2
Release:        %autorelease
Summary:        Link to GitHub issues, pull requests, commits and users from Sphinx docs
License:        BSD-2-Clause
URL:            https://github.com/jupyter/sphinxcontrib_github_alt
Source:         %{pypi_source sphinxcontrib_github_alt}

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
Link to GitHub issues, pull requests, commits and users for a particular
project.
It's called 'alt' because sphinxcontrib-github already exists. IPython &
Jupyter projects have been using the syntax defined in this extension for
some time before we made it into its own package, so we didn't want to
switch to sphinxcontrib-github.}

%description %_description


%package -n     python3-sphinxcontrib-github-alt
Summary:        %{summary}
%py_provides python3-sphinxcontrib_github_alt

%description -n python3-sphinxcontrib-github-alt %_description


%prep
%autosetup -n sphinxcontrib_github_alt-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files sphinxcontrib_github_alt


%check
# there are no tests upstream
%pyproject_check_import


%files -n python3-sphinxcontrib-github-alt -f %{pyproject_files}
%doc README.rst
%license COPYING.md


%changelog
%autochangelog
