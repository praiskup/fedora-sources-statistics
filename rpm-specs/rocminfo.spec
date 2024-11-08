%global rocm_release 6.2
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

Name:       rocminfo
Version:    %{rocm_version}
%if 0%{?rhel} && 0%{?rhel} < 10
Release:    1%{?dist}
%else
Release:    %autorelease
%endif
Summary:    ROCm system info utility

License:    NCSA
URL:        https://github.com/ROCm/rocminfo
Source0:    %{url}/archive/rocm-%{version}.tar.gz
Patch0:     0001-adjust-CMAKE_CXX_FLAGS.patch
Patch1:     0002-fix-buildtype-detection.patch

ExclusiveArch:  x86_64

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  rocm-runtime-devel >= %{rocm_release}.0
BuildRequires:  python3-devel

# rocminfo calls lsmod to check the kernel mode driver status
Requires:       kmod

%description
ROCm system info utility

%prep
%autosetup -n %{name}-rocm-%{version} -p1

%{__python3} %{_rpmconfigdir}/redhat/pathfix.py -i %{__python3} rocm_agent_enumerator

%build
%cmake -DROCM_DIR=/usr
%cmake_build

%install
%cmake_install

#FIXME:
chmod 755 %{buildroot}%{_bindir}/*

%files
%doc README.md
%license License.txt
%{_bindir}/rocm_agent_enumerator
%{_bindir}/rocminfo
#Duplicated files:
%exclude %{_docdir}/*/License.txt

%changelog
%autochangelog
