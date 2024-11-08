%global forgeurl https://github.com/libimobiledevice/ideviceinstaller
%global commit 1431d42b568ee78161a41ed02df0de60dc1439d6
%global date 20240518
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:           ideviceinstaller
Version:        1.1.1^%{date}git%{shortcommit}
Release:        %autorelease
Summary:        Manage apps of iOS devices

License:        GPL-2.0-or-later
URL:            https://www.libimobiledevice.org/
Source:         %{forgeurl}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

BuildRequires:  libimobiledevice-devel
BuildRequires:  libplist-devel
BuildRequires:  libzip-devel

%description
The ideviceinstaller application allows interacting with the app installation
service of an iOS device.

%prep
%autosetup -p1 -n %{name}-%{commit}

%if %{defined commit}
echo %{version} > .tarball-version
%endif

%build
NOCONFIGURE=1 ./autogen.sh
%configure --disable-static
%make_build

%install
%make_install

%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/ideviceinstaller
%{_mandir}/man1/ideviceinstaller.1*

%changelog
%autochangelog
