%global forgeurl https://github.com/glotzerlab/gsd
Version:        3.3.2
%forgemeta

Name:           python-gsd
Release:        %autorelease
Summary:        Read and write GSD files for use with HOOMD-blue

License:        BSD-2-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  %{py3_dist pytest}

%global _description %{expand:
The GSD file format is the native file format for HOOMD-blue. GSD files store
trajectories of the HOOMD-blue system state in a binary file with efficient
random access to frames. GSD allows all particle and topology properties to vary
from one frame to the next. Use the GSD Python API to specify the initial
condition for a HOOMD-blue simulation or analyze trajectory output with a
script. Read a GSD trajectory with a visualization tool to explore the behavior
of the simulation.}

%description %_description

%package -n     python3-gsd
Summary:        %{summary}

%description -n python3-gsd %_description

%prep
%autosetup -p1 -n gsd-%{version}

sed -i 's/numpy>=2.0.0rc1/numpy/' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files gsd

%check
ln -s %{buildroot}%{python3_sitearch}/gsd/fl.cpython-%{python3_version_nodots}-%{python3_platform_triplet}.so gsd/
# reading little-endian files on big-endian is unsupported
# https://github.com/glotzerlab/gsd/issues/12
# https://kojipkgs.fedoraproject.org/work/tasks/4655/111424655/build.log
%pytest -v gsd \
    --basetemp=$(mktemp -d -p %{_tmppath}) \
%ifarch s390x
-k "not test_gsd_v1_read \
and not test_gsd_v1_upgrade_read \
and not test_gsd_v1_write \
and not test_gsd_v1_upgrade_write"
%endif


%files -n python3-gsd -f %{pyproject_files}
%{_bindir}/gsd


%changelog
%autochangelog
