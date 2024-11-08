%global pypi_name arpeggio
Name:           python-%{pypi_name}
Version:        2.0.2
Release:        %autorelease
Summary:        Packrat parser interpreter

License:        MIT
URL:            https://github.com/igordejanovic/Arpeggio
Source0:        %pypi_source Arpeggio

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(pytest-runner)

%description
Arpeggio is a recursive descent parser with memoization based on PEG grammars
(aka Packrat parser).

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Arpeggio is a recursive descent parser with memoization based on PEG grammars
(aka Packrat parser).


%generate_buildrequires
%pyproject_buildrequires -r

%prep
%autosetup -p1 -n Arpeggio-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pytest -v


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md AUTHORS.md CHANGELOG.md THANKS.md
%license LICENSE


%changelog
%autochangelog
