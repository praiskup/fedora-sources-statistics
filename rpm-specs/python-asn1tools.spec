%global pypi_name asn1tools

Name:          python-%{pypi_name}
Version:       0.167.0
Release:       %autorelease
BuildArch:     noarch
Summary:       ASN.1 parsing, encoding and decoding
License:       MIT
URL:           https://github.com/eerimoq/%{pypi_name}
VCS:           git:%{url}.git
Source0:       %{pypi_source %{pypi_name}}
Patch1:        python-asn1tools-0001-Revert-Fixes-for-pyparsing-3.1.2.patch
BuildRequires: python3-devel
BuildRequires: python3-diskcache
BuildRequires: python3-prompt-toolkit
BuildRequires: python3-pytest
# No python-bitstruct module available
ExcludeArch:   s390x

%description
%{summary}.

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name}
%{summary}.

%prep
%if (0%{?fedora} && 0%{?fedora} < 40)
%autosetup -p1 -n %{pypi_name}-%{version}
%else
%autosetup -p1 -n %{pypi_name}-%{version} -N
%endif

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%{_bindir}/asn1tools

%changelog
%autochangelog
