%global date 20240902
%global commit 67bc17ea79b4ff1b449053e5fcf3375ff6b30690
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# This requires perfetto which isn't packaged yet
# https://bugzilla.redhat.com/show_bug.cgi?id=2255751
%bcond tracing 0

# The tests reliably segfault
%bcond check 0

Name:           chromiumos-platform
Version:        0~%{date}git%{shortcommit}
Release:        %autorelease
Summary:        ChromiumOS Platform

License:        BSD-3-Clause
URL:            https://chromium.googlesource.com/chromiumos/platform2
Source:         %{url}/+archive/%{commit}.tar.gz
Patch:          0001-Revert-sommelier-bump-up-CROSS_DOMAIN_MAX_IDENTIFIER.patch
Patch:          0002-vm_tools-sommelier-align-mem-operations-to-16K.patch
Patch:          0003-vm_tools-sommelier-don-t-call-to-fixup_plane0.patch
Patch:          0004-vm_tools-sommelier-Do-not-assert-on-unsued-wayland-i.patch

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  protobuf-compiler
BuildRequires:  python3
BuildRequires:  python3dist(jinja2)
%if %{with tracing}
BuildRequires:  perfetto-sdk
%endif

%if %{with check}
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gtest)
%endif
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)

%description
This package provides the ChromiumOS platform, which includes daemons,
programs, and libraries that were written specifically for ChromiumOS.

%package -n     sommelier
Summary:        Nested Wayland compositor with support for X11 forwarding
Requires:       mesa-dri-drivers
Requires:       xorg-x11-server-Xwayland

%description -n sommelier
Sommelier is an implementation of a Wayland compositor that delegates
compositing to a "host" compositor. Sommelier includes a set of features that
allows it to run inside a tight jail or virtual machine.

Sommelier can run as service or as a wrapper around the execution of a program.
As a service, called the parent sommelier, it spawns new processes as needed to
service clients.

%prep
%autosetup -c -p1

%build
pushd vm_tools/sommelier
%meson \
  -Dxwayland_path="%{_bindir}/Xwayland" \
  -Dxwayland_gl_driver_path="%{_libdir}/dri" \
  -Dgamepad=true \
  -Dquirks=true \
%if %{with tracing}
  -Dtracing=true \
%endif
%if %{without check}
  -Dwith_tests=false \
%endif
  %{nil}
%meson_build
popd

%install
pushd vm_tools/sommelier
%meson_install
popd

%if %{with check}
%check
pushd vm_tools/sommelier
%meson_test
popd
%endif

%files -n sommelier
%license LICENSE
%doc vm_tools/sommelier/README.md vm_tools/sommelier/TESTING.md
%doc vm_tools/sommelier/gaming.md
%{_bindir}/sommelier

%changelog
%autochangelog
