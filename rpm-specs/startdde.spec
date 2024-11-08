%bcond check 1

# https://github.com/linuxdeepin/startdde
%global goipath         github.com/linuxdeepin/startdde
Version:                6.0.15
%global tag             6.0.15

%gometa -L

%global common_description %{expand:
Startdde is used for launching DDE components and invoking user's custom
applications which compliant with xdg autostart specification.}

%global golicenses    LICENSE
%global godocs        README.md

Name:           startdde
Release:        %autorelease
Summary:        Starter of deepin desktop environment
License:        GPL-3.0-or-later
URL:            %{gourl}
Source:         %{gosource}

BuildRequires:  systemd-rpm-macros
BuildRequires:  make
BuildRequires:  golang
BuildRequires:  jq
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  libXcursor-devel
BuildRequires:  libXfixes-devel
BuildRequires:  gtk3-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  libsecret-devel

Provides:       x-session-manager
Requires:       deepin-daemon
Requires:       procps
Requires:       deepin-desktop-schemas
Requires:       deepin-kwin
# for lspci command
Requires:       pciutils
Recommends:     deepin-qt5integration

%description
%{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

sed -i 's/sbin/bin/' Makefile
sed -i 's|startdde fix-xauthority-perm||' Makefile

%generate_buildrequires
%go_generate_buildrequires

%build
%gobuild -o startdde
for cmd in fix-xauthority-perm greeter-display-daemon; do
    %gobuild -o $cmd github.com/linuxdeepin/startdde/cmd/$cmd
done
%make_build

%install
%make_install
%find_lang %{name}

%post
xsOptsFile=/etc/X11/Xsession.options
update-alternatives --install /usr/bin/x-session-manager x-session-manager \
    /usr/bin/startdde 90 || true
if [ -f $xsOptsFile ];then
	sed -i '/^use-ssh-agent/d' $xsOptsFile
	if ! grep '^no-use-ssh-agent' $xsOptsFile >/dev/null; then
		echo no-use-ssh-agent >> $xsOptsFile
	fi
fi

%if %{with check}
%check
%gocheck
%endif

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/startdde
%{_bindir}/deepin-fix-xauthority-perm
%dir %{_datadir}/startdde
%{_datadir}/startdde/filter.conf
%{_datadir}/lightdm/lightdm.conf.d/60-deepin.conf
%{_prefix}/lib/deepin-daemon/greeter-display-daemon
%{_datadir}/glib-2.0/schemas/*
%{_userunitdir}/dde-display-task-refresh-brightness.service
%{_userunitdir}/dde-session-initialized.target.wants/dde-display-task-refresh-brightness.service

%changelog
%autochangelog
