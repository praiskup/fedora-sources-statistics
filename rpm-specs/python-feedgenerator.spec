%global sum Standalone version of Django's feedgenerator module


Name:       python-feedgenerator
Version:    2.1.0
Release:    %autorelease
Summary:    %{sum}

# Automatically converted from old format: BSD - review is highly recommended.
License:    LicenseRef-Callaway-BSD
URL:        https://github.com/getpelican/feedgenerator
Source0:    %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%description
FeedGenerator is a standalone version of Django’s feedgenerator module. It has
evolved over time, including an update for Py3K and numerous other
enhancements.

%package -n python3-feedgenerator
Summary:        %{sum}

%description -n python3-feedgenerator
FeedGenerator is a standalone version of Django’s feedgenerator module. It has
evolved over time, including an update for Py3K and numerous other
enhancements.

%prep
%autosetup -n feedgenerator-%{version}
# remove coverage related bits for pytest
echo > setup.cfg

rm -rf feedgenerator/django/utils/six.py

for f in feedgenerator/django/utils/*py;
do
    sed -i -e 's/from . import six/import six/' -e 's/from .six \(import .*$\)/from six \1/'  $f
done

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files feedgenerator

%check
%pytest


%files -n python3-feedgenerator -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
