Name:           python-opentelemetry-sdk-extension-aws
Version:        2.0.2
Release:        %autorelease
Summary:        AWS SDK extension for OpenTelemetry

License:        Apache-2.0
URL:            https://pypi.org/project/opentelemetry-sdk-extension-aws
Source:         %{pypi_source opentelemetry_sdk_extension_aws}

BuildArch:      noarch

BuildRequires:  dos2unix

BuildRequires:  python3-devel
# Test dependencies. The upstream git repository has a file
# test-requirements.txt, not included in the PyPI sdist, but it pins exact
# versions and includes many indirect dependencies.
BuildRequires:  %{py3_dist pytest}

%global common_description %{expand:
This library provides components necessary to configure the OpenTelemetry SDK
for tracing with AWS X-Ray.}

%description %{common_description}


%package -n python3-opentelemetry-sdk-extension-aws
Summary:        %{summary}

%description -n python3-opentelemetry-sdk-extension-aws %{common_description}


%prep
%autosetup -n opentelemetry_sdk_extension_aws-%{version}
dos2unix --keepdate README.rst


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


%files -n python3-opentelemetry-sdk-extension-aws -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
