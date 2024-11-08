%bcond_without  tests

%if %{defined fedora}
%bcond_without  docs
%endif

Name:           python-trustme
Version:        1.1.0
Release:        %autorelease
Summary:        #1 quality TLS certs while you wait, for the discerning tester
License:        MIT OR Apache-2.0
URL:            https://github.com/python-trio/trustme
# PyPI tarball is missing docs-requirements.in
Source:         %{url}/archive/v%{version}/trustme-%{version}.tar.gz

# Add AKI to child CA certificates
# https://github.com/python-trio/trustme/pull/642
#
# Fixes:
#
# python-trustme fails to build with Python 3.13: ssl.SSLError: [SSL:
# SSLV3_ALERT_CERTIFICATE_UNKNOWN] ssl/tls alert certificate unknown
# (_ssl.c:1033)
# https://bugzilla.redhat.com/show_bug.cgi?id=2272940
Patch:          %{url}/pull/642.patch

BuildArch:      noarch

%global common_description %{expand:
You wrote a cool network client or server.  It encrypts connections using TLS.
Your test suite needs to make TLS connections to itself.  Uh oh.  Your test
suite probably does not have a valid TLS certificate.  Now what?  trustme is a
tiny Python package that does one thing: it gives you a fake certificate
authority (CA) that you can use to generate fake TLS certs to use in your
tests.  Well, technically they are real certs, they are just signed by your CA,
which nobody trusts.  But you can trust it.  Trust me.}


%description %{common_description}


%package -n python3-trustme
Summary:        %{summary}
BuildRequires:  python3-devel


%description -n python3-trustme %{common_description}


%if %{with docs}
%package -n python-trustme-doc
Summary:        Documentation for %{name}


%description -n python-trustme-doc
Documentation for %{name}.
%endif


%prep
%autosetup -n trustme-%{version} -p1
sed -e '/coverage/d' -i test-requirements.in


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:test-requirements.in} %{?with_docs:docs-requirements.in}


%build
%pyproject_wheel

%if %{with docs}
PYTHONPATH=$PWD/src sphinx-build-3 docs/source html
%endif


%install
%pyproject_install
%pyproject_save_files trustme


%check
%if %{with tests}
%pytest --verbose
%else
%pyproject_check_import
%endif


%files -n python3-trustme -f %{pyproject_files}
%doc README.rst


%if %{with docs}
%files -n python-trustme-doc
%license LICENSE LICENSE.MIT LICENSE.APACHE2
%doc html
%endif


%changelog
%autochangelog
