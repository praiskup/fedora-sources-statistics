Name:           python-optking
Version:        0.3.0
Release:        4%{?dist}
Summary:        A Python version of the PSI4 geometry optimization program by R.A. King
License:        BSD-3-Clause
URL:            https://github.com/psi-rking/optking
Source0:        https://github.com/psi-rking/optking/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pint
BuildRequires:  psi4

%description
optking (also known as pyoptking) is a rewrite of the c++ optking
module in psi4. This rewrite was undertaken to enable future
development and for use with recent interoperability efforts
(e.g. MolSSI QCArchive and QCDB). optking is focused on optimization
of molecular geometries: finding minima, transition states, and
reaction paths. Current work is focused especially on expanding the
reaction path methods.

%package -n     python3-optking
Summary:        %{summary}
%{?python_provide:%python_provide python3-optking}

%description -n python3-optking
optking (also known as pyoptking) is a rewrite of the c++ optking
module in psi4. This rewrite was undertaken to enable future
development and for use with recent interoperability efforts
(e.g. MolSSI QCArchive and QCDB). optking is focused on optimization
of molecular geometries: finding minima, transition states, and
reaction paths. Current work is focused especially on expanding the
reaction path methods.

%prep
%setup -q -n optking-%{version}
# Remove bundled egg-info
rm -rf optking.*-info
# Remove test that requires internet access to pubchem
\rm optking/tests/test_frozen_internals.py

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install

%check
pytest -m "not long" optking

%files -n python3-optking
%license LICENSE
%doc README.rst
%{python3_sitelib}/optking
%{python3_sitelib}/OptKing*.dist-info

%changelog
* Wed Sep 04 2024 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.3.0-4
- Turn on tests.

* Mon Sep 02 2024 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.3.0-3
- Removed explicit requires.

* Mon Sep 02 2024 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.3.0-2
- Review fixes.

* Wed Aug 28 2024 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.3.0-1
- First release.
