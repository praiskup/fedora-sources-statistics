%global pypi_name py3exiv2

Name:           python3-exiv2
Version:        0.12.0
Release:        %autorelease
Summary:        Python3 bindings for the exiv2 library

# GPL-2.0-only:
#  - py3exiv2-0.12.0/src/pyexiv2/__init__.py
#  - py3exiv2-0.12.0/src/pyexiv2/exif.py
#  - py3exiv2-0.12.0/src/pyexiv2/iptc.py
#  - py3exiv2-0.12.0/src/pyexiv2/metadata.py
#  - py3exiv2-0.12.0/src/pyexiv2/preview.py
#  - py3exiv2-0.12.0/src/pyexiv2/utils.py
#  - py3exiv2-0.12.0/src/pyexiv2/xmp.py
# GPL-2.0-or-later:
#  - py3exiv2-0.12.0/src/exiv2wrapper.cpp
#  - py3exiv2-0.12.0/src/exiv2wrapper.hpp
#  - py3exiv2-0.12.0/src/exiv2wrapper_python.cpp
License:        GPL-2.0-only AND GPL-2.0-or-later
Url:            https://launchpad.net/py3exiv2
Source:         %{pypi_source}

BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  boost-python3-devel
BuildRequires:  pkgconfig(exiv2)

%description
python3-exiv2 is a Python 3 binding to exiv2, the C++ library for manipulation
of EXIF, IPTC and XMP image metadata. It is a python 3 module that allows your
scripts to read and write metadata (EXIF, IPTC, XMP, thumbnails) embedded in
image files (JPEG, TIFF, ...).

It is designed as a high-level interface to the functionalities offered by
libexiv2. Using python’s built-in data types and standard modules, it provides
easy manipulation of image metadata.

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -t

%build
# Workaround as there is no -lboost_python3
sed -i 's|boost_python3|boost_python%{python3_version_nodots}|' setup.py
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pyexiv2

%check
%pyproject_check_import

%files -f %{pyproject_files}
%doc README
%{python3_sitearch}/libexiv2python%{python3_ext_suffix}

%changelog
%autochangelog
