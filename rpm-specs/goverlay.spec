Name:           goverlay
Version:        1.2
Release:        %autorelease
Epoch:          1
Summary:        Project that aims to create a Graphical UI to help manage Linux overlays
ExclusiveArch:  %{fpc_arches}

License:        GPL-3.0-or-later
URL:            https://github.com/benjamimgois/goverlay
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         goverlay-enable-debuginfo-generation.patch

BuildRequires:  desktop-file-utils
BuildRequires:  fpc-srpm-macros
BuildRequires:  lazarus
BuildRequires:  lazarus-lcl-qt6
BuildRequires:  libappstream-glib
BuildRequires:  libglvnd-devel
BuildRequires:  make

Requires:       hicolor-icon-theme
Requires:       mangohud%{?_isa}
Requires:       mesa-libGLU
Requires:       qt6pas%{?_isa}

# git - Clone reshade repository
Recommends:     git%{?_isa}

Recommends:     mesa-demos%{?_isa}
Recommends:     vkBasalt%{?_isa}
Recommends:     vulkan-tools%{?_isa}

%description
GOverlay is an open source project aimed to create a Graphical UI to manage
Vulkan/OpenGL overlays. It is still in early development, so it lacks a lot of
features.

This project was only possible thanks to the other maintainers and
contributors that have done the hard work. I am just a Network Engineer that
really likes Linux and Gaming.


%prep
%autosetup -p1


%build
%set_build_flags
%make_build


%install
%make_install prefix=%{_prefix}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_libexecdir}/%{name}
%{_mandir}/man1/*.1*
%{_metainfodir}/*.xml


%changelog
%autochangelog
