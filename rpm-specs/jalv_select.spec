# Global variables for github repository
%global commit0 aab00aadee7e9ea498bc59c5cd819505fe8b8c1d
%global gittag0 master
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20231220

Name:    jalv_select
Epoch:   1
Version: 1.3.0^%{commitdate}git%{shortcommit0}
Release: %autorelease
Summary: A little gtkmm GUI to select lv2 plugins from a list and run them with jalv.
URL:     https://github.com/brummer10/jalv_select
License: Unlicense

Source0: https://github.com/brummer10/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: lv2-devel
BuildRequires: lilv-devel
BuildRequires: gtkmm3.0-devel
BuildRequires: desktop-file-utils

Requires: jalv
Requires: jalv-qt
Requires: jalv-gtk

%description
A little gtkmm GUI to select lv2 plugins from a list and run them with jalv.
Features:
* select jalv interpreter from combo box
* select LV2 plugin from list
* select preset to load from menu
* search plugins by regex or plugin class
* reload lilv world to catch new installed plugins or presets
* load plugin with selected preset
* minimize app to systray (global Hotkey SHIFT+ESCAPE)
* wake up app from systray (global Hotkey SHIFT+ESCAPE)
* left mouse click on systray to show or hide app
* right mouse click to show quit menu item
* command-line start-up options
* command-line runtime options
* keyboard shortcuts

%prep
%autosetup -n %{name}-%{commit0}

%build

%set_build_flags

%make_build PREFIX=%{_prefix}

%install

%make_install PREFIX=%{_prefix}

%find_lang jalv.select

desktop-file-install --vendor '' \
        --add-category=X-Sound \
        --add-category=Midi \
        --add-category=Sequencer \
        --add-category=X-Jack \
        --dir %{buildroot}%{_datadir}/applications \
        %{buildroot}%{_datadir}/applications/jalv.select.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/jalv.select.desktop

%files -f jalv.select.lang
%doc README.md LOCALISATION.md
%license LICENSE
%{_bindir}/jalv.select
%{_datadir}/applications/jalv.select.desktop
%{_datadir}/pixmaps/*.png
%{_mandir}/man1/jalv.select.*
%{_mandir}/fr/man1/jalv.select.*

%changelog
%autochangelog
