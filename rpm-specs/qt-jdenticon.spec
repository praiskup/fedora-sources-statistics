%global __provides_exclude_from ^%{_qt6_plugindir}/.*\\.so$

Name: qt-jdenticon
Version: 0.3.1
Release: %autorelease

License: MIT
Summary: Jdenticon Qt5 plugin
URL: https://github.com/Nheko-Reborn/%{name}
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: qt6-qtbase-devel

%description
Special Qt/C++14 port of Jdenticon distributed as a Qt plugin.

The eventual plan for this is that it will be made into a Qt library that can
be used in other applications with a command-line application for use as a
standalone generator.

%prep
%autosetup -p1

%build
%qmake_qt6 QtIdenticon.pro
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%if 0%{?flatpak}
# qtbase is part of runtime in /usr, this is built in /app
mv %{buildroot}/usr %{buildroot}/app
%endif

%files
%doc README.md
%license LICENSE
%{_qt6_plugindir}/libqtjdenticon.so

%changelog
%autochangelog
