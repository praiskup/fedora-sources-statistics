Name:           python-blurb
Version:        1.3.0
Release:        %autorelease
Summary:        Command-line tool to manage CPython Misc/NEWS.d entries

License:        BSD-3-Clause
URL:            https://github.com/python/blurb
Source:         %{pypi_source blurb %{version}}

BuildArch:      noarch

BuildRequires:  python3-devel

%description
Blurb is a tool designed to rid CPython core development of the scourge of
Misc/NEWS conflicts.


%package -n     python3-blurb
Summary:        %{summary}
Provides:       blurb = %{version}-%{release}

# Calls git in subprocess
Requires:       /usr/bin/git

%description -n python3-blurb
Blurb is a tool designed to rid CPython core development of the scourge of
Misc/NEWS conflicts.


%prep
%autosetup -p1 -n blurb-%{version}
# avoid code coverage dependencies
sed -i '/"pytest-cov"/d' pyproject.toml

# script in site-packages
sed -i '1d' src/blurb/blurb.py
chmod -x src/blurb/blurb.py


%generate_buildrequires
%pyproject_buildrequires -x tests


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l blurb


%check
%pytest -v

%{py3_test_envvars} blurb --help
%{py3_test_envvars} %{python3} -m blurb --help

%{py3_test_envvars} blurb test
%{py3_test_envvars} %{python3} -m blurb test


%files -n python3-blurb -f %{pyproject_files}
%doc README.md
%{_bindir}/blurb


%changelog
%autochangelog
