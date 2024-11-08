%global pypi_name pyopengltk

Name:           python-%{pypi_name}
Version:        0.0.4
Release:        %{autorelease}
Summary:        An OpenGL frame for pyopengl-tkinter based on ctype

License:        MIT
URL:            https://github.com/jonwright/pyopengltk
Source:         %{pypi_source %{pypi_name}}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-tkinter
BuildRequires:  libX11

%global _description %{expand:
Tkinter - OpenGL Frame using ctypes

An opengl frame for pyopengl-tkinter based on ctypes (no togl
compilation).

Collected together by Jon Wright, Jan 2018.}

%description %_description


%package -n python3-%{pypi_name}
Summary:        %{summary}
Requires:       python3-tkinter
Requires:       libX11

%description -n python3-%{pypi_name} %_description


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Remove MacOS and Windows modules
rm -vf pyopengltk/darwin.py pyopengltk/win32.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


%check
# Upstream doesn't provide tests
%pyproject_check_import


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
