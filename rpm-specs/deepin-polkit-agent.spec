%global repo dde-polkit-agent

Name:           deepin-polkit-agent
Version:        6.0.7
Release:        %autorelease
Summary:        Deepin Polkit Agent
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-polkit-agent
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake

BuildRequires:  cmake(DtkWidget)
BuildRequires:  cmake(DtkCore)
BuildRequires:  cmake(DtkTools)

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Concurrent)
# lrelease-qt5
BuildRequires:  qt5-linguist

BuildRequires:  pkgconfig(polkit-qt5-1)

%description
DDE Polkit Agent is the polkit agent used in Deepin Desktop Environment.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Header files and libraries for %{name}.

%prep
%autosetup -p1 -n %{repo}-%{version}

sed -i 's|lrelease|lrelease-qt5|' translate_generation.sh
sed -i 's|qdbusxml2cpp|qdbusxml2cpp-qt5|' CMakeLists.txt

%build
%cmake
%cmake_build

%install
%cmake_install

%find_lang %{repo} --with-qt
rm %{buildroot}%{_datadir}/dde-polkit-agent/translations/dde-polkit-agent.qm

%files -f %{repo}.lang
%doc README.md
%license LICENSE
%dir %{_prefix}/lib/polkit-1-dde
%{_prefix}/lib/polkit-1-dde/dde-polkit-agent

%files devel
%{_includedir}/dpa/

%changelog
%autochangelog
