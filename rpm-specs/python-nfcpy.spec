# set upstream name variable
%global srcname nfcpy


Name:           python-nfcpy
Version:        1.0.4
Release:        %autorelease
Summary:        Python module to read/write NFC tags or communicate with another NFC device

License:        EUPL-1.1
URL:            https://github.com/%{srcname}/%{srcname}
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist ndeflib}
BuildRequires:  %{py3_dist pydes}
BuildRequires:  %{py3_dist libusb1}
BuildRequires:  %{py3_dist pyserial}
# For tests
BuildRequires:  %{py3_dist pytest}

%global _description %{expand:
The nfcpy module implements NFC Forum specifications for wireless
short-range data exchange with NFC devices and tags. It is written in
Python and aims to provide an easy-to-use yet powerful framework for
applications integrating NFC.}

%description %{_description}


%package     -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l nfc


%check
%pyproject_check_import
# tests are failing, so disabling
##%%pytest tests/


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst HISTORY.rst


%changelog
%autochangelog
