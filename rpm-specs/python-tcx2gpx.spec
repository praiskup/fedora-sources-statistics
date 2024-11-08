%bcond_without tests

%global _description %{expand:
This module converts the Garmin tcx GPS file format to the
more commonly used gpx file format. Both formats are a form
of XML but there are some fields in the former that are not
present in the later. It uses two packages to do the grunt
work tcxparser and gpxpy.}

Name:           python-tcx2gpx
Version:        0.1.5
Release:        %autorelease
Summary:        Convert Garmin TPX to GPX

License:        GPL-3.0-only
URL:            https://gitlab.com/nshephard/tcx2gpx
Source0:        %{pypi_source tcx2gpx}
BuildArch:      noarch

%description %_description

%package -n python3-tcx2gpx
Summary:        %{summary}

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%description -n python3-tcx2gpx %_description

%prep
%autosetup -p1 -n tcx2gpx-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files tcx2gpx

%check
%if %{with tests}
%pytest
%endif
# additional test
%pyproject_check_import

%files -n python3-tcx2gpx -f %{pyproject_files}
%doc README.md
%{_bindir}/tcx2gpx

%changelog
%autochangelog
