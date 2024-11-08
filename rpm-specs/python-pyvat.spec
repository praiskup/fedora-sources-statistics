%global sname pyvat
%global owner iconfinder
%global forgeurl https://github.com/%{owner}/%{sname}
Version:    1.3.19
%forgemeta

Name:       python-%{sname}
Release:    %autorelease
Summary:    VAT validation and calculation for Python
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:    Apache-2.0
URL:        https://github.com/iconfinder/pyvat/
BuildArch:  noarch
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}
Source0:    %{forgesource}
# https://github.com/iconfinder/pyvat/commit/ac5c01ca458e6d498d7238e62586964a0c3e64ba.patch
Patch1: python-pyvat-FI-VAT-update.patch

BuildRequires:  python3-devel
Requires:       python3

%description
With EU VAT handling rules becoming ever more ridiculous and complicated,
businesses within the EU are faced with the complexity of having to
validate VAT numbers. pyvat was built for
Iconfinder's marketplace to handle just this problem.

%package -n python3-%{sname}
Summary:    %{summary}

%description -n python3-%{sname}
With EU VAT handling rules becoming ever more ridiculous and complicated,
businesses within the EU are faced with the complexity of having to
validate VAT numbers. pyvat was built for
Iconfinder's marketplace to handle just this problem.

%prep
%forgesetup
%autopatch -p1

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{sname}

# check
# These tests require unittest2 to run as the project is compatible with Python 2 versions
# unittest2 was intentially removed from Fedora repositories see https://bugzilla.redhat.com/show_bug.cgi?id=1794222

%files -n python3-%{sname} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
