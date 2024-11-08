Name:           python-defusedxml
Version:        0.7.1
Release:        %autorelease
Summary:        XML bomb protection for Python stdlib modules
License:        PSF-2.0
URL:            https://github.com/tiran/defusedxml
Source:         %{pypi_source defusedxml}

# Drop deprecated unittest.makeSuite()
# From https://github.com/tiran/defusedxml/commit/4e6cea5f5b
# (This no longer skips lxml tests when lxml is not installed.)
Patch:          drop-makeSuite.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-lxml

%global _description %{expand:
The defusedxml package contains several Python-only workarounds and fixes for
denial of service and other vulnerabilities in Python's XML libraries. In order
to benefit from the protection you just have to import and use the listed
functions / classes from the right defusedxml module instead of the original
module.}

%description %_description

%package -n python3-defusedxml
Summary:        %{summary}

%description -n python3-defusedxml %_description


%prep
%autosetup -p1 -n defusedxml-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l defusedxml


%check
%{py3_test_envvars} %{python3} tests.py


%files -n python3-defusedxml -f %{pyproject_files}
%doc README.txt README.html CHANGES.txt


%changelog
%autochangelog
