Name:           vakzination
Version:        23.01.0
Release:        8%{?dist}

License:        CC-PDDC AND Apache-2.0 AND LGPL-2.0-or-later AND CC0-1.0 AND BSD-3-Clause AND GPL-2.0-or-later AND FSFAP
Summary:        Vakzination manages your health certificates like vaccination, test, and recovery certificates.
Url:            https://invent.kde.org/plasma-mobile/vakzination
Source:         https://download.kde.org/stable/plasma-mobile/%{version}/vakzination-%{version}.tar.xz

ExclusiveArch:  %{java_arches}

BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gcc-c++
BuildRequires: kf5-rpm-macros

BuildRequires: cmake(KF5CalendarCore)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5Contacts)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5Kirigami2)
BuildRequires: cmake(KF5Mime)
BuildRequires: cmake(KF5Prison)
BuildRequires: cmake(KHealthCertificate)
BuildRequires: cmake(KPimItinerary)
BuildRequires: cmake(KPimPkPass)

BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Qml)
BuildRequires: cmake(Qt5QuickControls2)
BuildRequires: cmake(Qt5Svg)

%description
%{summary}.

%prep
%autosetup

%build
%cmake_kf5
%cmake_build

%install
%cmake_install
%find_lang %{name}
desktop-file-install --dir=%{buildroot}%{_kf5_datadir}/applications/ %{buildroot}/%{_kf5_datadir}/applications/org.kde.%{name}.desktop

%files -f %{name}.lang

%license LICENSES/*

%{_kf5_bindir}/%{name}

%{_kf5_datadir}/applications/org.kde.%{name}.desktop

%{_kf5_metainfodir}/org.kde.%{name}.metainfo.xml

%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.01.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.01.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 14 2023 Justin Zobel <justin.zobel@gmail.com> - 23.01.0-6
- Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.01.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Justin Zobel <justin.zobel@gmail.com> - 23.01.0-3
- rebuilt

* Thu May 04 2023 Justin Zobel <justin@1707.io> - 23.01.0-2
- Rebuild

* Mon Jan 30 2023 Justin Zobel <justin@1707.io> - 23.01.0-1
- Update to 23.01.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Justin Zobel <justin@1707.io> - 22.11-1
- Update to 22.11

* Wed Sep 28 2022 Justin Zobel <justin@1707.io> - 22.09-1
- Update to 22.09

* Fri Aug 26 2022 Justin Zobel <justin@1707.io> - 22.06-1
- Update to 22.06

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 04 2022 Justin Zobel <justin@1707.io> - 22.04-1
- Update to 22.04

* Mon Feb 21 2022 Justin Zobel <justin@1707.io> - 22.02
- Verison bump to 22.02

* Wed Dec 22 2021 Justin Zobel <justin@1707.io> - 21.12-1
- Initial version of package
