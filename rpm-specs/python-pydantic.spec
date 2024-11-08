%bcond tests 1

Name:           python-pydantic
Version:        2.9.2
%global srcversion %{lua:return(rpm.expand("%{version}"):gsub("~",""))}
Release:        %autorelease
Summary:        Data validation using Python type hinting

# SPDX
License:        MIT
URL:            https://github.com/pydantic/pydantic
Source:         %{url}/archive/v%{srcversion}/pydantic-%{srcversion}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  tomcli
# For check phase
%if %{with tests}
BuildRequires:  %{py3_dist cloudpickle}
BuildRequires:  %{py3_dist dirty-equals}
BuildRequires:  %{py3_dist jsonschema}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-mock}
BuildRequires:  %{py3_dist pytz}
# Required for test_pretty_print
BuildRequires:  %{py3_dist rich}
%endif

%global _description %{expand:
Data validation and settings management using python type hinting.}

%description %{_description}


%package -n     python3-pydantic
Summary:        %{summary}
Recommends:     python3-pydantic+email
# The dotenv extra was removed in pydantic v2.
# Remove the Obsoletes in Fedora 43+
Obsoletes:      python3-pydantic+dotenv < 2~~

%description -n python3-pydantic %{_description}


%package        doc
Summary:        Documentaton for Pydantic

%description    doc
This package includes the documentation for Pydantic in Markdown format.


%prep
%autosetup -n pydantic-%{srcversion} -p1

# Delete pytest addopts. We don't care about benchmarking or coverage.
tomcli-set pyproject.toml del 'tool.pytest.ini_options.addopts'
# CPython 3.13 warns on FutureRef._evaluate/typing._eval_type not passing
# type_params
# https://github.com/pydantic/pydantic/issues/9613
#
#   DeprecationWarning: Failing to pass a value to the 'type_params' parameter
#   of 'typing._eval_type' is deprecated, as it leads to incorrect behaviour
#   when calling typing._eval_type on a stringified annotation that references
#   a PEP 695 type parameter. It will be disallowed in Python 3.15.
tomcli-set pyproject.toml append 'tool.pytest.ini_options.filterwarnings' \
    'ignore:Failing to pass a value.*PEP 695.*:DeprecationWarning:'


%generate_buildrequires
%pyproject_buildrequires -x email -x dotenv


%build
%pyproject_wheel


# Docs are in MarkDown, and should be added when mkdocs is packaged.

%install
%pyproject_install
%pyproject_save_files -l pydantic


%check
%pyproject_check_import -e pydantic.mypy -e pydantic.v1.mypy
%if %{with tests}
# We don't build docs or care about benchmarking
%pytest --ignore=tests/{test_docs.py,benchmarks} -k "${k-}" -rs
%endif


%files -n python3-pydantic -f %{pyproject_files}
%doc CITATION.cff
%doc HISTORY.md
%doc README.md

# Note that the timezone extra has no dependencies on our platform.
%pyproject_extras_subpkg email timezone -n python3-pydantic

%files doc
%license LICENSE
%doc docs/*

%changelog
%autochangelog
