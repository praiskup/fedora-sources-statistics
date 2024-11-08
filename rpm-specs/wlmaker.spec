# libbase is a utility library from the same upstream that is only used by this
# project and is statically linked into the build
%global libbase_commit 27aae1898bcc9bd125f260c42c370896159afbee
%global libbase_url https://github.com/phkaeser/libbase

%bcond docs 1

Name:           wlmaker
Version:        0.2
Release:        %autorelease
Summary:        Wayland compositor inspired by Window Maker

License:        Apache-2.0
URL:            https://github.com/phkaeser/wlmaker
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{libbase_url}/archive/%{libbase_commit}/libbase-%{libbase_commit}.tar.gz

# i686: https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
# ppc64le: https://github.com/phkaeser/libbase/issues/7
ExcludeArch:    %{ix86} ppc64le

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  sed
%if %{with docs}
BuildRequires:  doxygen
BuildRequires:  plantuml
%endif

# For libbase
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig(cairo) >= 1.16.0

# For wlmaker
BuildRequires:  pkgconfig(wayland-client) >= 1.22.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.31
BuildRequires:  pkgconfig(wayland-server) >= 1.22.0
BuildRequires:  pkgconfig(wlroots) >= 0.17
BuildRequires:  pkgconfig(xcb) >= 1.14
BuildRequires:  pkgconfig(xkbcommon) >= 1.0.3

# These are currently hardcoded in the dock
Recommends:     chromium
Recommends:     firefox
Recommends:     foot

%if %{with docs}
Suggests:       %{name}-doc = %{version}-%{release}
%endif

%description
Wayland Maker is a Wayland compositor inspired by Window Maker.

Key features:
- Compositor for windows in stacking mode.
- Supports multiple workspaces.
- Appearance inspired by Window Maker, following the look and feel of NeXTSTEP.
- Easy to use, lightweight, low gimmicks and fast.
- Dock and clip, to be extended for dockable apps.

%package        doc
Summary:        Developer documentation for %{name}
BuildArch:      noarch

%description    doc
This package provides additional developer documentation for %{name}.

%prep
%autosetup -p1 -b 1

# Drop bundled dependencies
rm -r dependencies

# Ensure libbase can be found; we move instead of symlinking because the build
# uses relative paths for the includes and that confuses things
rm -r submodules/libbase
mv ../libbase-%{libbase_commit}/ submodules/libbase

# Relax wayland version requirement
# https://github.com/phkaeser/wlmaker/issues/23
sed -i 's/1.22.90/1.22.0/g' CMakeLists.txt

# Do not abort on warnings
sed -i 's/-Werror//' CMakeLists.txt submodules/libbase/CMakeLists.txt

# Use chromium instead of google-chrome
sed -i 's/google-chrome/chromium-browser/' src/dock.c

%build
%cmake -Dconfig_OPTIM=ON
%cmake_build
%if %{with docs}
%cmake_build --target doc
%endif

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md CODE_OF_CONDUCT.md CONTRIBUTING.md doc/ROADMAP.md
%{_bindir}/wlmaker
%{_bindir}/wlmclock
%{_datadir}/icons/%{name}/

%if %{with docs}
%files doc
%license LICENSE
%doc %{_vpath_builddir}/doc/html/
%endif

%changelog
%autochangelog
