%global forgeurl https://github.com/swharden/pyABF

Name:           python-pyABF
Version:        2.3.8
Release:        %autorelease
Summary:        Python library for reading files in Axon Binary Format
%global tag %{version}
%forgemeta
# SPDX
License:        MIT
URL:            https://swharden.com/pyabf
Source:         %forgesource

# python-pyABF: FTBFS on s390x (big-endian)
# https://bugzilla.redhat.com/show_bug.cgi?id=2256818
#
# It *may* be that the package works fine on big-endian architectures, but only
# for big-endian data files. Without further investigation, it’s probably best
# not to offer the package to big-endian users.
ExcludeArch:    s390x
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%global _description %{expand:
pyABF provides a Python interface to electrophysiology files in the
Axon Binary Format (ABF). pyABF supports Python 3 and does not use
obscure libraries (just numpy and matplotlib). pyABF supports reading
ABF1 and ABF2 files and can write ABF1 files.}

%description %_description


%package -n python3-pyABF
Summary:        %{summary}

%description -n python3-pyABF %_description


%prep
%forgeautosetup -p1

# `pytest` is listed as runtime requirement, but it's only needed for
# running te tests. Remove it from `setup.py`
sed -i '/pytest/ d' src/setup.py


%generate_buildrequires
cd src/
%pyproject_buildrequires 


%build
cd src/
%pyproject_wheel


%install
cd src/
%pyproject_install
%pyproject_save_files -l pyabf


%check
%pytest -v --runslow


%files -n python3-pyABF -f %{pyproject_files}
%doc README.*

%changelog
%autochangelog
