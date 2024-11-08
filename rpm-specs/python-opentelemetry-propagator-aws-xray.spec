Name:           python-opentelemetry-propagator-aws-xray
Version:        1.0.2
Release:        %autorelease
Summary:        AWS X-Ray Propagator for OpenTelemetry

License:        Apache-2.0
URL:            https://pypi.org/project/opentelemetry-propagator-aws-xray
Source:         %{pypi_source opentelemetry_propagator_aws_xray}

BuildArch:      noarch

BuildRequires:  dos2unix

BuildRequires:  python3-devel
# Test dependencies. The upstream git repository has a file
# test-requirements.txt, not included in the PyPI sdist, but it pins exact
# versions and includes many indirect dependencies.
BuildRequires:  %{py3_dist opentelemetry-sdk}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist requests}

%global common_description %{expand:
This library provides the propagator necessary to inject or extract a tracing
context across AWS services.}

%description %{common_description}


%package -n python3-opentelemetry-propagator-aws-xray
Summary:        %{summary}

%description -n python3-opentelemetry-propagator-aws-xray %{common_description}


%prep
%autosetup -p1 -n opentelemetry_propagator_aws_xray-%{version}
dos2unix --keepdate README.rst


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# The opentelemetry and opentelemetry/propagators directies are shared
# namespace package directories; they are co-owned with other opentelemetry
# packages, including subpackages of python-opentelemetry and/or
# python-opentelemetry-contrib. See RHBZ#1935266.
%pyproject_save_files -l opentelemetry


%check
%pytest -v


%files -n python3-opentelemetry-propagator-aws-xray -f %{pyproject_files}
%doc README.rst


%changelog
%autochangelog
