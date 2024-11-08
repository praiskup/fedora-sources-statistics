# Tests depend on pytest-jupyter and that depends back
# on jupyter-server[test] so we might need to break this loop.
%bcond_without tests

Name:           python-jupyter-server
Version:        2.14.2
Release:        %autorelease
Summary:        The backend for Jupyter web applications
License:        BSD-3-Clause
URL:            https://jupyter-server.readthedocs.io
Source:         %{pypi_source jupyter_server}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
The Jupyter Server provides the backend (i.e. the core services,
APIs, and REST endpoints) for Jupyter web applications like
Jupyter notebook, JupyterLab, and Voila.}


%description %_description

%package -n     python3-jupyter-server
Summary:        %{summary}

%description -n python3-jupyter-server %_description


%prep
%autosetup -n jupyter_server-%{version}
sed -i '/"pre-commit"/d' pyproject.toml
# overrides is not available in Fedora
sed -i '/"overrides.*"/d' pyproject.toml
sed -i '/from overrides import overrides/d' jupyter_server/services/kernels/kernelmanager.py
sed -i '/@overrides/d' jupyter_server/services/kernels/kernelmanager.py

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-x test}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files jupyter_server


%check
%if %{with tests}
# ResourceWarning is flaky and causes some test to fail
# reported: https://github.com/jupyter-server/jupyter_server/issues/1387
# PytestUnraisableExceptionWarning added to the same report.
%pytest -vv -W "always:unclosed <socket.socket:ResourceWarning" -W "always::pytest.PytestUnraisableExceptionWarning"
%endif


%files -n python3-jupyter-server -f %{pyproject_files}
%doc README.md
%{_bindir}/jupyter-server

%pyproject_extras_subpkg -n python3-jupyter-server test


%changelog
%autochangelog
