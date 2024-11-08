%global srcname openpaperwork-core
%global srcname_ openpaperwork_core

Name:           python-%{srcname}
Version:        2.2.5
Release:        %autorelease
Summary:        OpenPaperwork's core

License:        GPL-3.0-or-later
URL:            https://gitlab.gnome.org/World/OpenPaperwork/paperwork/tree/master/openpaperwork-core
Source0:        %pypi_source %{srcname_}

BuildArch:      noarch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

BuildRequires:  python3-devel
BuildRequires:  python3-psutil

%description
Paperwork is a GUI to make papers searchable.

This is the core part of Paperwork. It manages plugins.


%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname}
Paperwork is a GUI to make papers searchable.

This is the core part of Paperwork. It manages plugins.


%prep
%autosetup -n %{srcname_}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{srcname_}

%check
%{py3_test_envvars} %{python3} -m unittest discover --verbose -s tests

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md ChangeLog

%changelog
%autochangelog
