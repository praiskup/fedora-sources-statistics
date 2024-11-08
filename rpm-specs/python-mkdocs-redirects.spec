Name:           python-mkdocs-redirects
Version:        1.2.1
Release:        %autorelease
Summary:        MkDocs plugin for dynamic page redirects to prevent broken links
BuildArch:      noarch

License:        MIT
URL:            https://github.com/datarobot/mkdocs-redirects
Source:         %{pypi_source mkdocs-redirects}

BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%description
A MkDocs plugin for dynamic page redirects to prevent broken links.


%package -n python3-mkdocs-redirects
Summary:        %{summary}


%description -n python3-mkdocs-redirects
A MkDocs plugin for dynamic page redirects to prevent broken links.


%prep
%autosetup -p1 -n mkdocs-redirects-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%check
%pytest


%install
%pyproject_install
%pyproject_save_files mkdocs_redirects


%files -n python3-mkdocs-redirects -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
