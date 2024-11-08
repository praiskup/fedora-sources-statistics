%global commit0 f13be9425328ebc579cafe90884ff6618af1db61
%global date 20240916
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

Name:           egl-x11
Version:        1.0.0%{!?tag:^%{date}git%{shortcommit0}}
Release:        1%{?dist}
Summary:        NVIDIA XLib and XCB EGL Platform Library
License:        Apache-2.0
URL:            https://github.com/NVIDIA/egl-x11

%if 0%{?tag:1}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif
# Allow building with an older meson:
Patch0:         egl-x11-meson-0.58.patch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(eglexternalplatform) >= 1.2
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm) >= 21.3.0
BuildRequires:  pkgconfig(libdrm) >= 2.4.99
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
# Minimum version 1.17.0 for explicit sync support (Fedora 40+):
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)

# Required for directory ownership
Requires:       libglvnd-egl%{?_isa}

%description
This is an EGL platform library for the NVIDIA driver to support XWayland via
xlib (using EGL_KHR_platform_x11) or xcb (using EGL_EXT_platform_xcb).

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

%build
%meson \
  -D xcb=true \
  -D xlib=enabled
%meson_build

%install
%meson_install

rm -fv %{buildroot}%{_libdir}/*.so

mv %{buildroot}%{_datadir}/egl/egl_external_platform.d/{xcb-platform.json,20_nvidia_xcb.json}
mv %{buildroot}%{_datadir}/egl/egl_external_platform.d/{xlib-platform.json,20_nvidia_xlib.json}

%files
%license LICENSE
%doc README.md
%{_libdir}/libnvidia-egl-xcb.so.1
%{_libdir}/libnvidia-egl-xcb.so.1.0.0
%{_libdir}/libnvidia-egl-xlib.so.1
%{_libdir}/libnvidia-egl-xlib.so.1.0.0
%{_datadir}/egl/egl_external_platform.d/20_nvidia_xcb.json
%{_datadir}/egl/egl_external_platform.d/20_nvidia_xlib.json

%changelog
* Wed Sep 18 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0^20240916gitf13be94-1
- Update to latest snapshot.

* Thu Sep 12 2024 Simone Caronni <negativo17@gmail.com> - 0.1^20240910git4b333d9-1
- Update to latest packaging guidelines for snapshots.

* Wed Sep 04 2024 Simone Caronni <negativo17@gmail.com> - 0.1-1.20240828git2be2296
- First build.
