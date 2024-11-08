Name:           python-pkg-depgraph
Version:        0.0.1.post1
Release:        %autorelease
Summary:        Packaging-oriented dependency graph library

License:        GPL-2.0-or-later
URL:            https://pagure.io/michel-slm/pkg-depgraph
Source:         %{pypi_source pkg_depgraph}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
Packaging-oriented dependency graph library.}

%description %_description

%package -n     python3-pkg-depgraph
Summary:        %{summary}

%description -n python3-pkg-depgraph %_description


%prep
%autosetup -p1 -n pkg_depgraph-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files pkg_depgraph


%check
%pyproject_check_import


%files -n python3-pkg-depgraph -f %{pyproject_files}


%changelog
%autochangelog
