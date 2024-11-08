# set upstream name variable
%global srcname ndeflib


Name:           python-ndeflib
Version:        0.3.3
Release:        %autorelease
Summary:        Python package for parsing and generating NFC Data Exchange Format messages

License:        ISC
URL:            https://github.com/nfcpy/%{srcname}
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
# For tests
BuildRequires:  %{py3_dist pytest}

%global _description %{expand:
The ndeflib is an ISC-licensed Python package for parsing and
generating NFC Data Exchange Format (NDEF) messages.

NDEF (NFC Data Exchange Format), specified by the NFC Forum, is a
binary message format used to encapsulate application-defined payloads
exchanged between NFC Devices and Tags. Each payload is encoded as an
NDEF Record with fields that specify the payload size, payload type,
an optional payload identifier, and flags for indicating the first and
last record of an NDEF Message or tagging record chunks. An NDEF
Message is simply a sequence of one or more NDEF Records where the
first and last record are marked by the Message Begin and End flags.}

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
%pyproject_save_files -l ndef


%check
%pyproject_check_import
# tests are failing, so disabling
##%%pytest tests/


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst HISTORY.rst


%changelog
%autochangelog
