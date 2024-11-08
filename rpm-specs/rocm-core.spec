%global upstreamname rocm-core
%global rocm_release 6.2
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

Name:           rocm-core
Version:        %{rocm_version}
Release:        %autorelease
Summary:        A utility to get the ROCm release version
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  clang

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
%{summary}

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

%build
%cmake -DROCM_VERSION=%{rocm_version}
%cmake_build

%install
%cmake_install

rm -rf %{buildroot}/%{_prefix}/.info
rm -rf %{buildroot}/%{_libdir}/rocmmod
rm -rf %{buildroot}/%{_docdir}/*/LICENSE.txt
rm -rf %{buildroot}/%{_libexecdir}/%{name}

mv  %{buildroot}/%{_includedir}/%{name}/*.h %{buildroot}/%{_includedir}/
rm -rf %{buildroot}/%{_includedir}/%{name}

%files
%license copyright
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/lib%{name}.so

%changelog
%autochangelog
