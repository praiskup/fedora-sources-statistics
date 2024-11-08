%global pypi_name multibase
%global common_description %{expand:
Multibase is a protocol for distinguishing base encodings and other simple
string encodings, and for ensuring full compatibility with program interfaces.

It answers the question: Given data d encoded into string s, how can I tell
what base d is encoded with?}

Name:          python-%{pypi_name}
Version:       1.0.3
Release:       %autorelease
BuildArch:     noarch
Summary:       Multibase implementation in Python
License:       MIT
URL:           https://github.com/multiformats/py-%{pypi_name}
VCS:           git:%{url}.git
Source0:       %{pypi_source py-%{pypi_name}}
# https://github.com/multiformats/py-multibase/pull/16
Patch1:        python-multibase-0001-Fix-issues-with-py.test.patch
BuildRequires: python3-devel
BuildRequires: python3-pytest

%description %{common_description}

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -p1 -n py-%{pypi_name}-%{version}

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
%doc AUTHORS.rst HISTORY.rst README.rst

%changelog
%autochangelog
