Name:           python-nudatus
Version:        0.0.5
Release:        %autorelease
Summary:        Strip comments from Python scripts

# SPDX
License:        MIT
URL:            https://github.com/zanderbrown/nudatus
Source:         %{url}/archive/%{version}/nudatus-%{version}.tar.gz

# Python 3.12 support, proposed upstream
Patch:          https://github.com/ZanderBrown/nudatus/pull/11.patch

BuildArch:      noarch

BuildRequires:  python3-devel
# test requirements mixed with coverage upstream, BRing pytest manually is easier
BuildRequires:  python3dist(pytest)

%description
Nudatus is a tool to remove comments from python scripts. It's created for use
in uflash to help squeeze longer programs onto the micro:bit but it should be
suitable for various environments with restricted storage.

%package -n     python3-nudatus
Summary:        %{summary}

Provides:       nudatus == %{version}-%{release}

%description -n python3-nudatus
Nudatus is a tool to remove comments from python scripts. It's created for use
in uflash to help squeeze longer programs onto the micro:bit but it should be
suitable for various environments with restricted storage.


%prep
%autosetup -p1 -n nudatus-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files nudatus

%check
%pytest -vvv tests

%files -n python3-nudatus -f %{pyproject_files}
%doc README.rst
%{_bindir}/nudatus

%changelog
%autochangelog
