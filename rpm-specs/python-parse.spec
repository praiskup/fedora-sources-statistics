%global srcname parse

Name:           python-%{srcname}
Version:        1.20.2
Release:        %autorelease
Summary:        Opposite of format()

License:        MIT
URL:            http://pypi.python.org/pypi/parse
Source:         %{pypi_source %{srcname}}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}

%global _description %{expand:
Parse strings using a specification based on the Python format() syntax.

"parse()" is the opposite of "format()"}

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{srcname}

%check
%pytest -v

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
