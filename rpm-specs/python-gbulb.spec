%global srcname gbulb

Name:           python-%{srcname}
Version:        0.6.5
Release:        %autorelease
Summary:        GLib event loop for tulip (PEP 3156)

License:        Apache-2.0
URL:            https://github.com/beeware/gbulb
Source:         %{pypi_source}
# upstream hardcodes arbitrary versions in dependencies to make their live
# easier (and harder for anybody else...); relax dependencies
Patch:          requirements-versions.patch
Patch:          0001-Fix-compatibility-with-Python-3.13.patch

BuildArch:      noarch
BuildRequires:  gtk3-devel
BuildRequires:  python3-devel

%global _description %{expand:
Gbulb is a Python library that implements a PEP 3156 interface for the GLib
main event loop under UNIX-like systems.}

%description %_description

%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%tox

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst AUTHORS.rst CHANGELOG.rst

%changelog
%autochangelog
