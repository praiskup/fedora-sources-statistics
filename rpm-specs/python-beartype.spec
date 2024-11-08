Name:           python-beartype
Version:        0.18.5
Release:        %autorelease
Summary:        Unbearably fast runtime type checking in pure Python
License:        MIT
URL:            https://beartype.readthedocs.io
Source:         %{pypi_source beartype}
# Python 3.13 backport
Patch:          4b27fbb518cabad406132b0fc321028ddb26d829.patch
Patch:          e07f8ee04819e27e11270c33777649586c6f4d87.patch
Patch:          0b4453f83c7ed4be054d8733aab8075e1478e166.patch
Patch:          c8c4f05d49ac1dd240a7325652404ed995004eb9.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest) 
BuildRequires:  python3dist(sphinx)
BuildRequires:  make

%global _description %{expand:
An open-source pure-Python PEP-compliant near-real-time hybrid
runtime-static third-generation type checker emphasizing efficiency,
usability, unsubstantiated jargon we just made up, and thrilling puns.}

%description %_description

%package -n     python3-beartype
Summary:        %{summary}

%description -n python3-beartype %_description

%prep
%autosetup -p1 -n beartype-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel
(cd doc; make man singlehtml)

%install
%pyproject_install
%pyproject_save_files beartype
install -m0644 -D doc/trg/man/beartype.1 %{buildroot}%{_mandir}/man1/beartype.1
gzip %{buildroot}%{_mandir}/man1/beartype.1
mv doc/trg/singlehtml/index.html beartype.html
# https://github.com/beartype/beartype/issues/331
find %{buildroot}/%{python3_sitelib} -type f -name \*.py -print0 | xargs -0  sed -i "s:#\!/usr/bin/env python3:# :"

%check
%pyproject_check_import
%pytest beartype_test

%files -n python3-beartype -f %{pyproject_files}
%license LICENSE
%doc beartype.html
%{_mandir}/man1/beartype.1.*

%changelog
%autochangelog
