# Owns: /usr/lib/python3.10/site-packages/keyrings/__init__.py
# So keep an eye out for any other packages that may also want to own it.

%bcond tests 1

%global _description %{expand:
Alternate keyring backend implementations for use with the keyring package.

Keyrings in this package may have security risks or other implications. These
backends were extracted from the main keyring project to make them available
for those who wish to employ them, but are discouraged for general production
use. Include this module and use its backends at your own risk.

For example, the PlaintextKeyring stores passwords in plain text on the file
system, defeating the intended purpose of this library to encourage best
practices for security.}

%global forgeurl  https://github.com/jaraco/keyrings.alt

Name:           python-keyrings-alt
Version:        5.0.2
Release:        %{autorelease}
Summary:        Alternate keyring implementations

%forgemeta

# SPDX
License:        MIT
URL:            %forgeurl
Source:         %forgesource

BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  gnome-keyring
# The following are from the test extra, but it also contains linting/coverage
# tools that we don’t want. It’s easier to depend manually on the things that
# we need than to patch out the things that we don’t.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist keyring}
BuildRequires:  %{py3_dist pycryptodomex}
%endif

%description %_description

%package -n python3-keyrings-alt
Summary:        %{summary}
# Not included in install_requires
Requires:       %{py3_dist keyring}
Provides:       python-keyrings-alt-doc = %{version}-%{release}
Obsoletes:      python-keyrings-alt-doc < %{version}-2

%description -n python3-keyrings-alt %_description

%prep
%forgesetup

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_install
%pyproject_save_files -l keyrings

%check
%if %{with tests}
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
# Skip integration tests with python-crypto/PyCrypto; prefer pycryptodomex.
k="${k-}${k+ and }not [Crypto]"
%pytest -k "${k-}"
%endif

%files -n python3-keyrings-alt -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
