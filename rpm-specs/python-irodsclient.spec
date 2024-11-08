Name:           python-irodsclient
Version:        2.2.0
Release:        %autorelease
Summary:        A python API for iRODS

# SPDX
License:        BSD-3-Clause
URL:            https://github.com/irods/python-irodsclient
Source:         %{pypi_source python-irodsclient}

BuildArch:      noarch

BuildRequires:  python3-devel

%global common_description %{expand:
iRODS (https://www.irods.org/) is an open source distributed data management
system. This is a client API implemented in Python.}

%description %{common_description}


%package -n python3-irodsclient
Summary:        %{summary}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-irods

%description -n python3-irodsclient %{common_description}


%prep
%autosetup -n python-irodsclient-%{version} -p1
# Remove useless shebangs in files that will be installed without executable
# permission. The pattern of selecting files before modifying them with sed
# keeps us from unnecessarily discarding the original mtimes on unmodified
# files.
find 'irods' -type f -name '*.py' \
    -exec gawk '/^#!/ { print FILENAME }; { nextfile }' '{}' '+' |
  xargs -r sed -r -i '1{/^#!/d}'


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l irods


%check
# * The test runner module requires xmlrunner, which is no longer packaged.
# * Merely importing ssl_test_client requires configured iRODS credentials.
%pyproject_check_import -e irods.test.runner -e irods.test.ssl_test_client
# All tests require network access and a valid account on a running iRODS grid.
# See irods/test/README.rst.


%files -n python3-irodsclient -f %{pyproject_files}
%doc CHANGELOG.md
%doc README.md


%changelog
%autochangelog
