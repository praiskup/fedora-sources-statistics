%global git_commit 0642a71126c32cd26b3a443a5cac27e4e1f7240f
%global pypi_name morphys
%global common_description %{expand:
Smart conversions between unicode and bytes types for common cases in python.}

Name:          python-%{pypi_name}
Version:       1.0
Release:       %autorelease
BuildArch:     noarch
Summary:       Smart conversions between unicode and bytes types
License:       MPL-2.0
URL:           https://github.com/mkalinski/%{pypi_name}
VCS:           git:%{url}.git
Source0:       %{url}/archive/%{git_commit}/morphys-1.0.tar.gz
BuildRequires: python3-devel

%description %{common_description}

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{git_commit}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
%pyproject_check_import
%python3 ./tests.py

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
