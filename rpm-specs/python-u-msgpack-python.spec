%global pypi_name u-msgpack-python

Name:           python-%{pypi_name}
Version:        2.8.0
Release:        %autorelease
Summary:        A portable, lightweight MessagePack serializer and deserializer

License:        MIT
URL:            https://github.com/vsergeev/u-msgpack-python
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel

%description
A lightweight MessagePack serializer and deserializer module written in pure
Python. It is fully compliant with the latest MessagePack specification.
In particular, it supports the new binary, UTF-8 string, and
application-defined ext types.


%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
A lightweight MessagePack serializer and deserializer module written in pure
Python. It is fully compliant with the latest MessagePack specification.
In particular, it supports the new binary, UTF-8 string, and
application-defined ext types.


%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files umsgpack


%check
%tox


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
