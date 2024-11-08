Name:           deepin-screenshot
Version:        5.0.0
Release:        %autorelease
Summary:        Deepin Screenshot Tool
Summary(zh_CN): 深度截图工具
# Automatically converted from old format: GPLv3 - review is highly recommended.
License:        GPL-3.0-only
Url:            https://github.com/linuxdeepin/deepin-screenshot
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-appdata.xml
# follow changes from Arch
Patch0:         https://raw.githubusercontent.com/archlinux/svntogit-community/e244b11755511b0eb84636302993a84a7bc7273c/trunk/deepin-screenshot-no-notification.patch

BuildRequires:  cmake
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(dtkwm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       desktop-file-utils
Requires:       hicolor-icon-theme
Recommends:     deepin-shortcut-viewer

%description
Provide a quite easy-to-use screenshot tool. Features:
  * Global hotkey to triggle screenshot tool
  * Take screenshot of a selected area
  * Easy to add text and line drawings onto the screenshot

%description -l zh_CN
简单易用的截图工具. 特性:
  * 支持全局热键激活截图工具
  * 支持区域截图
  * 支持为截图添加文本和图形

%prep
%setup -q
# fix for Qt 5.15
sed -i '1i #include <QPainterPath>' src/widgets/shapeswidget.cpp
# Disable using deepin-turbo, which is not yet available in Fedora
sed -i 's/deepin-turbo-invoker.*deepin/deepin/' \
       src/dbusservice/com.deepin.Screenshot.service deepin-screenshot.desktop

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix}
%cmake_build

%install
%cmake_install
install -Dm644 %SOURCE1 %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop ||:
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml

%preun
if [ $1 -eq 0 ]; then
  /usr/sbin/alternatives --remove x-window-screenshot %{_bindir}/%{name}
fi

%post
if [ $1 -eq 1 ]; then
  /usr/sbin/alternatives --install %{_bindir}/x-window-screenshot \
    x-window-screenshot %{_bindir}/%{name} 20
fi

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/dbus-1/services/com.deepin.Screenshot.service
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
%autochangelog
