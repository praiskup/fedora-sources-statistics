Name:           dtkmultimedia
Version:        1.0.7
Release:        %autorelease
Summary:        Development Tool Kit Multimedia

# most of the files are under GPL-2.0-or-later AND LGPL-3.0-or-later, except:

# src/ocr/ppocr/postprocess_op.cpp: Apache-2.0
# src/ocr/ppocr/postprocess_op.h: Apache-2.0
# src/ocr/ppocr/utility.cpp: Apache-2.0
# src/ocr/ppocr/utility.h: Apache-2.0

# src/ocr/ppocr/clipper.cpp: BSL-1.0
# src/ocr/ppocr/clipper.hpp: BSL-1.0
License:        Apache-2.0 AND BSL-1.0 AND GPL-2.0-or-later AND LGPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dtkmultimedia
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# Link ffmpeg libraries to fix build
# Fix build failure if compiler check return type
Patch0:         https://github.com/linuxdeepin/dtkmultimedia/pull/56.patch
# Port to FFmpeg 7
Patch1:         %{name}-ffmpeg7.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5MultimediaWidgets)
BuildRequires:  cmake(Qt5X11Extras)

BuildRequires:  pkgconfig(dtkcore)
BuildRequires:  pkgconfig(dtkwidget)
BuildRequires:  pkgconfig(dbusextended-qt5)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(ncnn)
BuildRequires:  pkgconfig(opencv)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavdevice)

BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(mpv)
BuildRequires:  pkgconfig(libffmpegthumbnailer)
BuildRequires:  libusb1-devel
BuildRequires:  portaudio-devel
BuildRequires:  libv4l-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  libXtst-devel

%description
Development Tool Kit (DtkMultimedia) is the base development tool of all C++/Qt
Developer work on Deepin.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%package -n     libdtkocr
Summary:        Library files for libdtkocr
Requires:       libdtkocr-data = %{version}-%{release}

%description -n libdtkocr
This package contains library files for libdtkocr.

%package -n     libdtkocr-data
Summary:        Data files for libdtkocr
BuildArch:      noarch

%description -n libdtkocr-data
This package contains data files for libdtkocr.

%package -n     libdtkocr-devel
Summary:        Development files for libdtkocr
Requires:       libdtkocr%{?_isa} = %{version}-%{release}

%description -n libdtkocr-devel
This package contains development files for libdtkocr.

%prep
%autosetup -p1
# '-Wl,--as-needed' already included in LDFLAGS when building on Fedora
sed -i '/-Wl,--as-needed/d' CMakeLists.txt
sed -i 's/opencv_mobile/opencv4/g' src/ocr/CMakeLists.txt
sed -i 's/qhelpgenerator/qhelpgenerator-qt5/g' docs/CMakeLists.txt

%build
export CFLAGS="%{build_cflags} -Wno-implicit-function-declaration"
%cmake -DBUILD_DOCS=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSES/*
%doc README.md
%{_libdir}/libdtkmultimedia.so.1*
%{_libdir}/libdtkmultimediawidgets.so.1*

%files devel
%{_libdir}/libdtkmultimedia.so
%{_libdir}/libdtkmultimediawidgets.so
%{_includedir}/dtkmultimedia/
%{_includedir}/dtkmultimediawidgets/
%{_libdir}/cmake/dtkmultimedia/
%{_libdir}/pkgconfig/dtkmultimedia.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_dtkmultimedia.pri

%files -n libdtkocr
%{_libdir}/libdtkocr.so.1*

%files -n libdtkocr-data
%dir %{_datadir}/libdtkocr
%{_datadir}/libdtkocr/dtkocrmodels/

%files -n libdtkocr-devel
%{_libdir}/libdtkocr.so
%{_includedir}/dtkocr/
%{_libdir}/cmake/dtkocr/
%{_libdir}/pkgconfig/dtkocr.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_dtkocr.pri

%changelog
%autochangelog
