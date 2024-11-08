Name:           qaccessibilityclient-qt5
Summary:        Accessibility client library for Qt5
Version:        0.6.0
Release:        %autorelease
License:        CC0-1.0 AND LGPL-2.1-only AND LGPL-3.0-only AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:            https://invent.kde.org/libraries/libqaccessibilityclient
Source0:        %{url}/-/archive/v%{version}/libqaccessibilityclient-v%{version}.tar.bz2

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros

BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5DBus)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}-qt5
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
%{summary}.

%prep
%autosetup -p1 -n libqaccessibilityclient-v%{version}

%build
%cmake_kf5
%cmake_build

%install
%cmake_install

%files
%doc AUTHORS README.md
%license LICENSES/*
%{_libdir}/libqaccessibilityclient-qt5.so.0*
%{_datadir}/qlogging-categories5/libqaccessibilityclient.categories

%files devel
%{_includedir}/QAccessibilityClient/
%{_libdir}/cmake/QAccessibilityClient/
%{_libdir}/libqaccessibilityclient-qt5.so

%changelog
%autochangelog
