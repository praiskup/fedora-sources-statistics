%bcond check 1

# https://github.com/linuxdeepin/dde-api
%global goipath         github.com/linuxdeepin/dde-api
Version:                6.0.11
%global tag             6.0.11

%gometa -L

Name:           deepin-api
Release:        %autorelease
Summary:        Go-lang bingding for dde-daemon
License:        GPL-3.0-or-later
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(polkit-qt5-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  deepin-gettext-tools
BuildRequires:  make
BuildRequires:  systemd-rpm-macros
%{?systemd_requires}

Requires:       deepin-desktop-base
Requires:       rfkill

%description
%{summary}.

%package -n     golang-deepin-api-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n golang-deepin-api-devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%prep
%goprep -A
%autopatch -p1

sed -i 's|boot/grub/|boot/grub2/|' adjust-grub-theme/main.go

# add targets to print the binaries and libraries, so we can build/install them
# in Fedora style
cat <<EOF >> Makefile
print_binaries:
	@echo \${BINARIES}

print_libraries:
	@echo \${LIBRARIES}
EOF

%generate_buildrequires
%go_generate_buildrequires

%build
make prepare
# upstream Makefile expects binaries generated to out/bin
for cmd in $(make print_binaries); do
    %gobuild -o out/bin/$cmd %{goipath}/$cmd
done
# don't build binaries or libraries based on Makefile
%make_build ts-to-policy

%install
# install dev libraries mannally
gofiles=$(find $(make print_libraries) %{?gofindfilter} -print)
%goinstall $gofiles
# install binaries based on Makefile
make DESTDIR=%{buildroot} SYSTEMD_SERVICE_DIR="%{_unitdir}" GOBUILD_DIR=_build install-binary
install -pDm 0644 archlinux/%{name}.sysusers %{buildroot}%{_sysusersdir}/%{name}.conf

# Move sound-theme-player to %%{libexec}/%%{name} to get proper SELinux type
mkdir -p %{buildroot}%{_libexecdir}/%{name}
mv -v %{buildroot}%{_prefix}/lib/%{name}/sound-theme-player \
      %{buildroot}%{_libexecdir}/%{name}
ln -s ../../libexec/%{name}/sound-theme-player \
      %{buildroot}%{_prefix}/lib/%{name}/sound-theme-player

%if %{with check}
%check
%gocheck
%endif

%pre
%sysusers_create_compat archlinux/%{name}.sysusers

%post
%systemd_post deepin-shutdown-sound.service

%preun
%systemd_preun deepin-shutdown-sound.service

%postun
%systemd_postun_with_restart deepin-shutdown-sound.service

%files
%doc README.md
%license LICENSE
%{_bindir}/dde-open
%dir %{_libexecdir}/deepin-api
%{_libexecdir}/deepin-api/sound-theme-player
%dir %{_prefix}/lib/deepin-api
%{_prefix}/lib/deepin-api/*
%{_unitdir}/*.service
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/icons/hicolor/*/actions/*
%dir %{_datadir}/dde-api
%dir %{_datadir}/dde-api/data
%dir %{_datadir}/dde-api/data/grub-themes
%{_datadir}/dde-api/data/grub-themes/deepin-fallback/
%{_datadir}/dde-api/data/grub-themes/deepin/
%{_datadir}/dde-api/data/huangli.db
%{_datadir}/dde-api/data/huangli.version
%{_datadir}/dde-api/data/pkg_depends
%{_datadir}/polkit-1/actions/*.policy
%{_var}/lib/polkit-1/localauthority/10-vendor.d/org.deepin.dde.device.pkla
%{_sysusersdir}/deepin-api.conf

%files -n golang-deepin-api-devel -f devel.file-list

%changelog
%autochangelog
