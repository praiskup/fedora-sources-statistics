# This package corresponds to two PyPI projects (fastapi-cli-slim, and
# fastapi-cli) co-developed in one repository. Since the two are versioned
# identically and released at the same time, it makes sense to build them from
# a single source package. (The fastapi-slim and fastapi packages are versioned
# and packaged separately.) The two published PyPI sdists differ only in their
# pyproject.toml files: they have different names, and some of the dependencies
# for fastapi-cli-slim belong to an optional extra.

Name:           fastapi-cli
Version:        0.0.5
Release:        %autorelease
Summary:        Run and manage FastAPI apps from the command line with FastAPI CLI

License:        MIT
URL:            https://github.com/fastapi/fastapi-cli
# The GitHub archive contains a few useful files that the PyPI sdist does not,
# such as the release notes.
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Written for Fedora in groff_man(7) format based on --help output
Source10:       fastapi.1
Source11:       fastapi-dev.1
Source12:       fastapi-run.1

# Downstream-only: run test_script without coverage
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
Patch:          0001-Downstream-only-run-test_script-without-coverage.patch

BuildArch:      noarch

%py_provides python3-fastapi-cli
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_requiring_base_package
Requires:       fastapi-cli-slim = %{version}-%{release}

BuildRequires:  python3-devel

# Since requirements-tests.txt contains overly-strict version bounds and many
# unwanted linting/coverage/typechecking/formatting dependencies
# (https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters),
# we just list the few test dependencies we *do* want manually rather than
# trying to patch the requirements file. We preserve upstream’s lower bounds
# but remove upper bounds, as we must try to make do with what we have.
BuildRequires:  %{py3_dist pytest} >= 4.4
BuildRequires:  %{py3_dist fastapi-slim}
BuildRequires:  %{py3_dist uvicorn}

%global common_description %{expand:
FastAPI CLI is a command line program fastapi that you can use to serve your
FastAPI app, manage your FastAPI project, and more.}

%description %{common_description}


%pyproject_extras_subpkg -n fastapi-cli -i %{python3_sitelib}/fastapi_cli-%{version}.dist-info standard


%package slim
Summary:        %{summary}

%py_provides python3-fastapi-cli-slim

%description slim %{common_description}


%pyproject_extras_subpkg -n fastapi-cli-slim -i %{python3_sitelib}/fastapi_cli_slim-%{version}.dist-info standard


%prep
%autosetup -p1


%generate_buildrequires
export TIANGOLO_BUILD_PACKAGE='fastapi-cli-slim'
%pyproject_buildrequires -x standard
(
  export TIANGOLO_BUILD_PACKAGE='fastapi-cli'
  %pyproject_buildrequires
) | grep -vE '\bfastapi-cli\b'


%build
export TIANGOLO_BUILD_PACKAGE='fastapi-cli-slim'
%pyproject_wheel
export TIANGOLO_BUILD_PACKAGE='fastapi-cli'
%pyproject_wheel


%install
%pyproject_install

install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 \
    '%{SOURCE10}' '%{SOURCE11}' '%{SOURCE12}'

install -d \
    '%{buildroot}%{bash_completions_dir}' \
    '%{buildroot}%{zsh_completions_dir}' \
    '%{buildroot}%{fish_completions_dir}'
export PYTHONPATH='%{buildroot}%{python3_sitelib}'
export _TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION=1
'%{buildroot}%{_bindir}/fastapi' --show-completion bash \
    > '%{buildroot}%{bash_completions_dir}/fastapi'
'%{buildroot}%{_bindir}/fastapi' --show-completion zsh \
    > '%{buildroot}%{zsh_completions_dir}/_fastapi'
'%{buildroot}%{_bindir}/fastapi' --show-completion fish \
    > '%{buildroot}%{fish_completions_dir}/fastapi.fish'


%check
%pytest -k "${k-}" ${ignore-} -v


%files
%{python3_sitelib}/fastapi_cli-%{version}.dist-info/


%files slim
%license LICENSE
%doc CITATION.cff
%doc README.md
%doc release-notes.md

%{_bindir}/fastapi
%{_mandir}/man1/fastapi.1*
%{_mandir}/man1/fastapi-*.1*
%{bash_completions_dir}/fastapi
%{zsh_completions_dir}/_fastapi
%{fish_completions_dir}/fastapi.fish

%{python3_sitelib}/fastapi_cli/
%{python3_sitelib}/fastapi_cli_slim-%{version}.dist-info/


%changelog
%autochangelog
