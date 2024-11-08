Name:           python-parso
Version:        0.8.4
Release:        %autorelease
Summary:        Parser that supports error recovery and round-trip parsing
License:        MIT AND PSF-2.0
BuildArch:      noarch
URL:            https://github.com/davidhalter/parso
Source:         %{pypi_source parso}

%global common_description %{expand:
Parso is a Python parser that supports error recovery and round-trip parsing
for different Python versions (in multiple Python versions). Parso is also able
to list multiple syntax errors in your python file.  Parso has been
battle-tested by jedi. It was pulled out of jedi to be useful for other
projects as well.  Parso consists of a small API to parse Python and analyse
the syntax tree.}


%description %{common_description}


%package -n python3-parso
Summary:        %{summary}
BuildRequires:  python3-devel


%description -n python3-parso %{common_description}


%prep
%autosetup -p 1 -n parso-%{version}

sed -e '/^addopts/d' -i pytest.ini


%generate_buildrequires
%pyproject_buildrequires -x testing


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files parso


%check
# According to upstream, the error tests are "very susceptible to failures and
# might break from time to time".  They recommend skipping them during distro
# package builds.
# https://github.com/davidhalter/parso/issues/63
# https://github.com/davidhalter/parso/issues/103
# https://github.com/davidhalter/parso/issues/123
# https://bugzilla.redhat.com/show_bug.cgi?id=1830965
# https://github.com/davidhalter/parso/issues/192
# https://github.com/davidhalter/parso/issues/222
%pytest --verbose -k "not test_python_exception_matches"


%files -n python3-parso -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
