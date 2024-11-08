%global mypaint_data_version 1.0

Name: mypaint-brushes
Epoch: 1
Version: 1.3.1
Release: %autorelease
Summary: Brushes to be used with the MyPaint library

# According to Licenses.dep5 the files used for building/installing are GPLv2+
# but the shipped brush files are CC0
License: CC0-1.0
URL: https://github.com/mypaint/mypaint-brushes
Source0: https://github.com/mypaint/mypaint-brushes/releases/download/v%{version}/mypaint-brushes-%{version}.tar.xz

BuildArch: noarch
BuildRequires: make


%package devel
Summary: Files for developing with mypaint-brushes
Requires: pkgconfig
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License: GPL-2.0-or-later


%description
This package contains brush files for use with MyPaint and other programs.


%description devel
This package contains a pkgconfig file which makes it easier to develop
programs using these brush files.


%prep
%autosetup


%build
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%doc AUTHORS NEWS README
%license COPYING
%dir %{_datadir}/mypaint-data
%dir %{_datadir}/mypaint-data/%{mypaint_data_version}
%{_datadir}/mypaint-data/%{mypaint_data_version}/brushes


%files devel
%license COPYING
%{_datadir}/pkgconfig/mypaint-brushes-%{mypaint_data_version}.pc


%changelog
%autochangelog
