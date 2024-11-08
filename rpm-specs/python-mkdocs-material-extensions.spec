Name:           python-mkdocs-material-extensions
Version:        1.3.1
Release:        %autorelease
Summary:        Extension pack for Python Markdown and MkDocs Material

License:        MIT
URL:            https://github.com/facelessuser/mkdocs-material-extensions
Source:         %{pypi_source mkdocs_material_extensions}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
This package provides Markdown extension resources for MkDocs Material.}

%description %_description

%package -n     python3-mkdocs-material-extensions
Summary:        %{summary}

%description -n python3-mkdocs-material-extensions %_description

%prep
%autosetup -p1 -n mkdocs_material_extensions-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files materialx

%check
%tox

%files -n python3-mkdocs-material-extensions -f %{pyproject_files}
%doc README.md

%changelog
%autochangelog
