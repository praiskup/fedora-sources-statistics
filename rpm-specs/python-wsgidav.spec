Name:           python-wsgidav
Version:        4.3.3
Release:        %autorelease
Summary:        Generic and extendable WebDAV server based on WSGI

# The entire source is (SPDX) MIT, except tests/davclient.py, which is
# Apache-2.0 (but does not contribute to the licenses of the binary RPMs).
License:        MIT
URL:            https://github.com/mar10/wsgidav
# The GitHub source includes a few ancillary files that the PyPI sdist lacks;
# for example, it contains tox.ini, which defines the test dependencies.
Source0:        %{url}/archive/v%{version}/wsgidav-%{version}.tar.gz
# Man page hand-written for Fedora in groff_man(7) format based on --help
Source1:        wsgidav.1

BuildArch:      noarch
BuildRequires:  python3-devel

%global common_description %{expand:
A generic and extendable WebDAV server written in Python and based on WSGI.

Main features:

  • WsgiDAV is a stand-alone WebDAV server with SSL support, that can be
    installed and run as Python command line script.
  • The python-pam library is needed as extra requirement if pam-login
    authentication is used on Linux or OSX.
  • WebDAV is a superset of HTTP, so WsgiDAV is also a performant,
    multi-threaded web server with SSL support.
  • WsgiDAV is also a Python library that implements the WSGI protocol and can
    be run behind any WSGI compliant web server.
  • WsgiDAV is implemented as a configurable stack of WSGI middleware
    applications. Its open architecture allows to extend the functionality and
    integrate WebDAV services into your project. Typical use cases are:
      • Expose data structures as virtual, editable file systems.
      • Allow online editing of MS Office documents.}

%description %{common_description}


%package -n python3-wsgidav
Summary:        %{summary}

%description -n python3-wsgidav %{common_description}


%pyproject_extras_subpkg -n python3-wsgidav pam


%prep
%autosetup -n wsgidav-%{version}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
# - pytest-cov is a coverage tool
# - pytest-html is not packaged, and is only used for generating reports
sed -r -i 's/^([[:blank:]]*)(pytest-(cov|html)\b)/\1# \2/' tox.ini
%if v"0%{?python3_version}" >= v"3.13"
# python-webob fails to build with Python 3.13: ModuleNotFoundError: No module
# named 'cgi'
# https://bugzilla.redhat.com/show_bug.cgi?id=2245641
#
# DeprecationWarning: 'cgi' is deprecated and slated for removal in Python 3.13
# https://github.com/Pylons/webob/issues/437
#
# The webtest test dependency depends on webob, which does not support Python
# 3.13.
sed -r -i 's/^([[:blank:]]*)(webtest\b)/\1# \2/' tox.ini
%endif


%generate_buildrequires
%pyproject_buildrequires -x pam -t


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l wsgidav

install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 '%{SOURCE1}'


%check
%if v"0%{?python3_version}" >= v"3.13"
ignore="${ignore-} --ignore=tests/test_wsgidav_app.py"
%endif
# While tox.ini is useful for generating test dependencies, it also attempts to
# pip-install pytest-html. Rather than patching this out (and patching out the
# pytest arguments related to pytest-cov and pytest-html), we just run pytest
# directly.
%pytest -ra -v -x ${ignore-}


%files -n python3-wsgidav -f %{pyproject_files}
%doc CHANGELOG.md
%doc README.md

%{_bindir}/wsgidav
%{_mandir}/man1/wsgidav.1*


%changelog
%autochangelog
