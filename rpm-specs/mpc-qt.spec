%global app_id  io.github.mpc_qt.Mpc-Qt

Name:           mpc-qt
Version:        24.06
Release:        %autorelease
Summary:        A clone of Media Player Classic reimplemented in Qt
# MainWindow::on_actionHelpAbout_triggered states "or later"
# qthelper.hpp is ISC
License:        GPL-2.0-or-later AND ISC
URL:            https://mpc-qt.github.io/
Source0:        https://github.com/mpc-qt/mpc-qt/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{app_id}.appdata.xml

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  pkgconfig(mpv)
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  qt6-linguist

Requires:       hicolor-icon-theme

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

%description
Media Player Classic Home Cinema (mpc-hc) is considered by many to be the
quintessential media player for the Windows desktop.
Media Player Classic Qute Theater (mpc-qt) aims to reproduce most of the
interface and functionality of mpc-hc.

%prep
%autosetup -p1
rm -rf mpv-dev


%build
%qmake_qt6 MPCQT_VERSION=%{version} PREFIX=%{_prefix}
%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}
rm -f %{buildroot}%{_datadir}/doc/mpc-qt/ipc.md
install -D -m0644 %{SOURCE1} %{buildroot}%{_metainfodir}/%{app_id}.appdata.xml


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{app_id}.appdata.xml


%files
%doc README.md DOCS/ipc.md
%license LICENSE
%{_bindir}/mpc-qt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_metainfodir}/%{app_id}.appdata.xml


%changelog
%autochangelog
