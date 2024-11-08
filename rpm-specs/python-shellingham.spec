Name:           python-shellingham
Version:        1.5.4
Release:        %autorelease
Summary:        Tool to detect surrounding Shell
License:        ISC
URL:            https://github.com/sarugaku/shellingham
Source0:        %{url}/archive/%{version}/shellingham-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-mock

%description
Shellingham detects what shell the current Python executable is running in.

%package -n     python3-shellingham
Summary:        %{summary}

%description -n python3-shellingham
Shellingham detects what shell the current Python executable is running in.


%prep
%autosetup -n shellingham-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l shellingham

%check
%pytest -v

%files -n python3-shellingham -f %{pyproject_files}
%doc README.rst CHANGELOG.rst

%changelog
%autochangelog
