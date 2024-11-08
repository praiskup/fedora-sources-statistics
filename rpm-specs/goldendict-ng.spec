%global tag 24.05.05-LiXia.ecd1138c	
Version:        %(echo %{tag} | awk -F'-' '{print $1}')

Name:           goldendict-ng
Release:        %autorelease
Summary:        The Next Generation GoldenDict

# The program is licensed under the GPL-3.0-or-later, except some files:
# src/{dictzip.hh,dictzip.c} - GPL-1.0-or-later
# src/dict/{bgl_babylon.hh,bgl_babylon.cc} - GPL-2.0-or-later
# src/dict/{ripemd.hh,ripemd.cc,mdictparser.hh,mdictparser.cc} - GPL-3.0-only
# files of JavaScript libraries:
# src/scripts/darkreader.js - MIT
# src/scripts/{iframeResizer.contentWindow.min.js,iframeResizer.min.js} - MIT
# src/scripts/jquery-3.6.0.slim.min.js - MIT
License:        GPL-3.0-or-later AND GPL-1.0-or-later AND GPL-2.0-or-later AND GPL-3.0-only AND MIT
URL:            https://github.com/xiaoyifang/goldendict-ng
Source0:        %{url}/archive/v%{tag}/goldendict-ng-%{tag}.tar.gz
Patch0:         https://github.com/xiaoyifang/goldendict-ng/commit/e2e1ca2d49b939e89a12104a2e9c90875a7d50ea.patch#/%{name}-ffmpeg7.patch

# https://src.fedoraproject.org/rpms/qt6-qtwebengine/blob/rawhide/f/qt6-qtwebengine.spec#_90
ExclusiveArch:  aarch64 x86_64

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build

BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6WebEngineWidgets)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  cmake(Qt6TextToSpeech)

BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(opencc)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(lzo2)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xapian-core)
BuildRequires:  pkgconfig(libzim)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(tomlplusplus)
# ffmpeg
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
# xz-devel
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  eb-devel

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Provides:       bundled(qtsingleapplication)
Provides:       bundled(js-darkreader)
Provides:       bundled(js-iframe-resizer)
Provides:       bundled(js-jquery)

%description
The Next Generation GoldenDict. A feature-rich open-source dictionary lookup
program, supporting multiple dictionary formats and online dictionaries.

%prep
%autosetup -p1 -n %{name}-%{tag}

# remove unneeded third-party libraries
rm -r thirdparty/{fmt,qwebengine_ts,tomlplusplus}
rm -r winlibs

%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_SYSTEM_FMT=ON \
    -DUSE_SYSTEM_TOML=ON \
    -DUSE_ALTERNATIVE_NAME=ON \
    -DCMAKE_SKIP_RPATH=ON
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/goldendict-ng
%{_datadir}/applications/io.github.xiaoyifang.goldendict_ng.desktop
%{_datadir}/pixmaps/goldendict-ng.png
%{_metainfodir}/io.github.xiaoyifang.goldendict_ng.metainfo.xml
%dir %{_datadir}/goldendict-ng
%dir %{_datadir}/goldendict-ng/locale
%{_datadir}/goldendict-ng/locale/*.qm

%changelog
%autochangelog
