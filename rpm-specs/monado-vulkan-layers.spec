%global forgeurl  https://gitlab.freedesktop.org/monado/utilities/vulkan-layers
%global commit    ae43cdcbd25c56e3481bbc8a0ce2bfcebba9f7c2
%global date      20240221
%forgemeta


Name:           monado-vulkan-layers
Version:        0.9.0
Release:        %autorelease
Summary:        Optional Vulkan Layers for Monado

# VkLayer_MND_enable_timeline_semaphore BSL-1.0
# misc helper/config scripts CC0-1.0
License:        BSL-1.0 AND CC0-1.0
URL:            %{forgeurl}
Source0:        %{forgesource}


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(vulkan)

Requires:       vulkan-loader


%description
Vulkan layers to support additional APIs via Monado.


%prep
%forgeautosetup -p1


%build
%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}/%{name}/layer \

%cmake_build


%install
%cmake_install


%files
%license LICENSE LICENSES/*
%{_libdir}/%{name}/layer/libVkLayer_MND_enable_timeline_semaphore.so
%{_datarootdir}/vulkan/implicit_layer.d/VkLayer_MND_enable_timeline_semaphore.json


%changelog
%autochangelog
