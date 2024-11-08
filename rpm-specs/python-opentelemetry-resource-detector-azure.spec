Name:           python-opentelemetry-resource-detector-azure
Version:        0.1.5
Release:        %autorelease
Summary:        OpenTelemetry Resource detectors for Azure

License:        Apache-2.0
URL:            https://pypi.org/project/opentelemetry-resource-detector-azure
Source:         %{pypi_source opentelemetry_resource_detector_azure}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}

%global common_description %{expand:
This library contains OpenTelemetry Resource Detectors for the following Azure
resources:

  • Azure App Service
  • Azure Virtual Machines}

%description %{common_description}


%package -n python3-opentelemetry-resource-detector-azure
Summary:        %{summary}

%description -n python3-opentelemetry-resource-detector-azure %{common_description}


%prep
%autosetup -n opentelemetry_resource_detector_azure-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# The opentelemetry and opentelemetry/sdk directies are shared
# namespace package directories; they are co-owned with other opentelemetry
# packages, including subpackages of python-opentelemetry and/or
# python-opentelemetry-contrib. See RHBZ#1935266.
%pyproject_save_files -l opentelemetry


%check
%pytest -v


%files -n python3-opentelemetry-resource-detector-azure -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
