%global extdir %{_datadir}/gnome-shell/extensions
%global gschemadir %{_datadir}/glib-2.0/schemas

Name:           gnome-shell-frippery
Version:        47.0
Release:        %autorelease
Summary:        Extensions to provide a user experience more like that of GNOME 2

License:        GPL-2.0-or-later
URL:            http://frippery.org/extensions
Source0:        %{url}/%{name}-%{version}.tgz

BuildArch:      noarch

Requires:       gnome-shell-extension-common

%description
This package contains some GNOME Shell extensions to provide a user experience
more like that of GNOME 2.

%package -n     gnome-shell-extension-frippery-applications-menu
Summary:        Replace Activities button with an Applications menu
%description -n gnome-shell-extension-frippery-applications-menu
This GNOME Shell extension replaces the Activities button in the panel with an
Applications menu.

%package -n     gnome-shell-extension-frippery-bottom-panel
Summary:        Add a bottom panel to the shell
%description -n gnome-shell-extension-frippery-bottom-panel
This GNOME Shell extension adds a bottom panel, including a window list and
workspace switcher.

%package -n     gnome-shell-extension-frippery-move-clock
Summary:        Move clock to left of status menu button
%description -n gnome-shell-extension-frippery-move-clock
This GNOME Shell extension moves the clock from the centre of the panel
towards the right.

%package -n     gnome-shell-extension-frippery-panel-favorites
Summary:        Add launchers for Favorites to the panel
%description -n gnome-shell-extension-frippery-panel-favorites
This GNOME Shell extension places a launcher for each favourite application in
the panel. Right clicking on the icons invokes a menu that lets one perform
various operations on the application.

%prep
%setup -q -c %{name}-%{version}
mv .local/share/gnome-shell/extensions .
mv .local/share/gnome-shell/gnome-shell-frippery/* .

%build

%install
mkdir -p %{buildroot}%{extdir}
cp -PR extensions/* %{buildroot}%{extdir}

# Install glib2 schema in the proper location
mkdir -p %{buildroot}%{gschemadir}
cp -P extensions/*/schemas/*.gschema.xml %{buildroot}%{gschemadir}
rm -r %{buildroot}%{extdir}/*/schemas

%find_lang frippery-applications-menu
%find_lang frippery-bottom-panel

%files -n gnome-shell-extension-frippery-applications-menu -f frippery-applications-menu.lang
%doc README CHANGELOG
%license COPYING
%{extdir}/Applications_Menu@rmy.pobox.com
%{gschemadir}/org.frippery.applications-menu.gschema.xml

%files -n gnome-shell-extension-frippery-bottom-panel -f frippery-bottom-panel.lang
%doc README CHANGELOG
%license COPYING
%{extdir}/Bottom_Panel@rmy.pobox.com
%{gschemadir}/org.frippery.bottom-panel.gschema.xml

%files -n gnome-shell-extension-frippery-move-clock
%doc README CHANGELOG
%license COPYING
%{extdir}/Move_Clock@rmy.pobox.com

%files -n gnome-shell-extension-frippery-panel-favorites
%doc README CHANGELOG
%license COPYING
%{extdir}/Panel_Favorites@rmy.pobox.com
%{gschemadir}/org.frippery.panel-favorites.gschema.xml

%changelog
%autochangelog
