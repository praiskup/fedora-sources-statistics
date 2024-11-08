Name:           dcm2niix
Version:        1.0.20220720
Release:        %autorelease
Summary:        DICOM to NIfTI converter

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            http://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage
Source0:        https://github.com/rordenlab/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz

# Patch for new yaml-cpp using CMake config files
# https://github.com/rordenlab/dcm2niix/issues/647
Patch0:         dcm2niix-yaml-cpp.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  nifticlib-devel
BuildRequires:  zlib-devel
BuildRequires:  turbojpeg-devel
BuildRequires:  git
BuildRequires:  yaml-cpp-devel
BuildRequires:  CharLS-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  python3-sphinx

Provides:       %{name}%{?_isa} = %{version}-%{release}

# console/ujpeg.{h,cpp}
# https://github.com/neurolabusc/dcm2niix/issues/8
Provides:       bundled(nanojpeg)

%description
dcm2niix is a tool designed to convert neuroimaging data from the NIfTI format
to the DICOM format.

%prep
%autosetup -p1 -n %{name}-%{version}
# Set executable name
sed -i 's/sphinx-build/sphinx-build-3/' docs/CMakeLists.txt

mkdir build/

%build
%cmake -DUSE_STATIC_RUNTIME=OFF -DUSE_TURBOJPEG=ON -DUSE_OPENJPEG=ON  -DUSE_JPEGLS=ON -DZLIB_IMPLEMENTATION=System -DBATCH_VERSION=ON -DBUILD_DOCS=ON
%cmake_build

%install
%cmake_install

%files
%doc README.md VERSIONS.md
%license license.txt
%{_bindir}/%{name}
%{_bindir}/dcm2niibatch
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/dcm2niibatch.1*


%changelog
%autochangelog
