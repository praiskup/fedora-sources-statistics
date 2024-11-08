%if ! 0%{?fedora} || 0%{?fedora} >= 41
%bcond gimp3 1
%else
%bcond gimp3 0
%endif

%if %{with gimp3}
%global gimpver 3.0
%else
%global gimpver 2.0
%endif

%global gimpdatadir %{_datadir}/gimp/%{gimpver}

Summary: Extra files for GIMP
Name: gimp-data-extras
Version: 2.0.4
Release: %autorelease
License: GPL-3.0-or-later
URL: https://www.gimp.org/
Source0: https://download.gimp.org/pub/gimp/extras/gimp-data-extras-%{version}.tar.bz2
Source1: org.gimp.GIMP.data_extras.metainfo.xml
Patch0: gimp-data-extras-2.0.4-gimp3.patch
BuildArch: noarch
ExcludeArch: s390x
BuildRequires: gimp-devel-tools
BuildRequires: gimp-devel >= 2:2.0
BuildRequires: make
Requires: gimp >= 2:2.0

%description
Patterns, gradients, and other extra files for GIMP.

%prep
%setup -q

%if %{with gimp3}
%patch 0 -p 1 -b .gimp3
%endif

%build
%configure
make

%install
%make_install

install -d -m 0755 %{buildroot}%{_datadir}/metainfo
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/metainfo/

%files
%doc AUTHORS ChangeLog NEWS README
%license COPYING
%{gimpdatadir}/*
%{_datadir}/metainfo/*.metainfo.xml

%changelog
%autochangelog
