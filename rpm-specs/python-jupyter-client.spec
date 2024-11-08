# Unset -s on python shebang - ensure that extensions installed with pip
# to user locations are seen and properly loaded
%undefine _py3_shebang_s

Name:           python-jupyter-client
Version:        8.6.1
Release:        %autorelease
Summary:        Jupyter protocol implementation and client libraries

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://jupyter.org
Source0:        %{pypi_source jupyter_client}

# Avoid a DeprecationWarning on Python 3.13+
Patch:          https://github.com/jupyter/jupyter_client/pull/1027.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%bcond_without doc
%bcond_without tests

%if %{with tests}
# The zmq tests are split in RPM only, the dependency is not tracked on Python level:
BuildRequires:  python3-zmq-tests
# Optional test dependency, look for test_datetimes_msgpack
BuildRequires:  python3dist(msgpack)
# For test_load_ips
BuildRequires:  /usr/sbin/ip
BuildRequires:  /usr/sbin/ifconfig
%endif

%description
This package contains the reference implementation of the Jupyter protocol.
It also provides client and kernel management APIs for working with kernels.

It also provides the `jupyter kernelspec` entrypoint for installing kernelspecs
for use with Jupyter frontends.

%package -n     python3-jupyter-client
Summary:        %{summary}

# It fallbacks to ifconfig without this, and ifconfig is deprecated
Recommends:     python3-netifaces

%description -n python3-jupyter-client
This package contains the reference implementation of the Jupyter protocol.
It also provides client and kernel management APIs for working with kernels.

It also provides the `jupyter kernelspec` entrypoint for installing kernelspecs
for use with Jupyter frontends.

%if %{with doc}
%package -n python-jupyter-client-doc
Summary:        Documentation of the Jupyter protocol reference implementation

%description -n python-jupyter-client-doc
Documentation of the reference implementation of the Jupyter protocol
%endif

%prep
%autosetup -p1 -n jupyter_client-%{version}
# Drop dependencies on coverage, linters etc.
sed -Ei '/"\b(codecov|coverage|mypy|pre-commit|pytest-cov)\b",/d' pyproject.toml


%if %{with doc}
# Use local objects.inv for intersphinx:
sed -i "s|\(('http://ipython.readthedocs.io/en/stable/', \)None)|\1'/usr/share/doc/python3-ipython-doc/html/objects.inv')|" docs/conf.py
%endif


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-x test} %{?with_doc:-x docs}


%build
%pyproject_wheel

%if %{with doc}
PYTHONPATH=build/lib/ sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -r html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install
%pyproject_save_files jupyter_client


%if %{with tests}
%check
# The two tests testing signals for kernels are flaky because
# if it takes the kernel more than one second to respond, it's killed.
# The tests work fine outside mock.
# test_open_tunnel needs ssh and internet connections.
%pytest -Wdefault -v -k "not test_signal_kernel_subprocesses and not test_async_signal_kernel_subprocesses and not test_open_tunnel"
%endif


%global _docdir_fmt %{name}

%files -n python3-jupyter-client -f %{pyproject_files}
%doc README.md
%{_bindir}/jupyter-kernel
%{_bindir}/jupyter-kernelspec
%{_bindir}/jupyter-run

%if %{with doc}
%files -n python-jupyter-client-doc
%doc html
%endif

%changelog
%autochangelog
