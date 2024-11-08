%global debug_package %{nil}

Name:           protozero
Version:        1.7.1
Release:        9%{?dist}
Summary:        Minimalistic protocol buffer decoder and encoder in C++

License:        BSD-2-Clause
URL:            https://github.com/mapbox/protozero
Source0:        https://github.com/mapbox/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake make gcc-c++
BuildRequires:  doxygen graphviz
BuildRequires:  protobuf-devel protobuf-lite-devel protobuf-compiler
BuildRequires:  catch2-devel

%description
Minimalistic protocol buffer decoder and encoder in C++.

Designed for high performance. Suitable for writing zero copy parsers
and encoders with minimal need for run-time allocation of memory.

Low-level: this is designed to be a building block for writing a
very customized decoder for a stable protobuf schema. If your protobuf
schema is changing frequently or lazy decoding is not critical for your
application then this approach offers no value: just use the decoding
API available via the C++ API that can be generated via the Google
Protobufs protoc program.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}

%description    devel
Minimalistic protocol buffer decoder and encoder in C++.

Designed for high performance. Suitable for writing zero copy parsers
and encoders with minimal need for run-time allocation of memory.

Low-level: this is designed to be a building block for writing a
very customized decoder for a stable protobuf schema. If your protobuf
schema is changing frequently or lazy decoding is not critical for your
application then this approach offers no value: just use the decoding
API available via the C++ API that can be generated via the Google
Protobufs protoc program.


%prep
%autosetup -p 1 -n %{name}-%{version}
rm -rf test/catch
ln -sf /usr/include/catch2 test/catch
mkdir build


%build
%cmake -DWERROR=OFF
%cmake_build


%install
%cmake_install


%check
%ctest


%files devel
%doc README.md doc/*.md %{__cmake_builddir}/doc/html
%license LICENSE.md LICENSE.from_folly
%{_includedir}/protozero


%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Mar 11 2023 Tom Hughes <tom@compton.nu> - 1.7.1-5
- Require catch2-devel instead of catch-devel

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Tom Hughes <tom@compton.nu> - 1.7.1-1
- Update to 1.7.1 upstream release

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 19 2021 Tom Hughes <tom@compton.nu> - 1.7.0-4
- Unbundle catch

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun  8 2020 Tom Hughes <tom@compton.nu> - 1.7.0-1
- Update to 1.7.0 upstream release

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Tom Hughes <tom@compton.nu> - 1.6.8-1
- Update to 1.6.8 upstream release

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 Tom Hughes <tom@compton.nu> - 1.6.7-1
- Update to 1.6.7 upstream release

* Wed Feb 20 2019 Tom Hughes <tom@compton.nu> - 1.6.6-1
- Update to 1.6.6 upstream release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 31 2019 Tom Hughes <tom@compton.nu> - 1.6.4-1
- Update to 1.6.4 upstream release

* Tue Jul 17 2018 Tom Hughes <tom@compton.nu> - 1.6.3-1
- Update to 1.6.3 upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar  9 2018 Tom Hughes <tom@compton.nu> - 1.6.2-1
- Update to 1.6.2 upstream release

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Tom Hughes <tom@compton.nu> - 1.6.1-2
- Build using catch1

* Sat Nov 18 2017 Tom Hughes <tom@compton.nu> - 1.6.1-1
- Update to 1.6.1 upstream release

* Wed Nov  1 2017 Tom Hughes <tom@compton.nu> - 1.6.0-1
- Update to 1.6.0 upstream release

* Sat Sep 23 2017 Tom Hughes <tom@compton.nu> - 1.5.3-1
- Update to 1.5.3 upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul  1 2017 Tom Hughes <tom@compton.nu> - 1.5.2-1
- Update to 1.5.2 upstream release

* Mon Feb 13 2017 Tom Hughes <tom@compton.nu> - 1.5.1-3
- Add patch for Catch 1.7.1 support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 14 2017 Tom Hughes <tom@compton.nu> - 1.5.1-1
- Update to 1.5.1 upstream release

* Thu Jan 12 2017 Tom Hughes <tom@compton.nu> - 1.5.0-1
- Update to 1.5.0 upstream release

* Sat Nov 19 2016 Tom Hughes <tom@compton.nu> - 1.4.5-1
- Update to 1.4.5 upstream release

* Tue Nov 15 2016 Tom Hughes <tom@compton.nu> - 1.4.4-1
- Update to 1.4.4 upstream release

* Sat Sep 10 2016 Tom Hughes <tom@compton.nu> - 1.4.2-2
- Rebuild to add aarch64 support

* Sat Sep 10 2016 Tom Hughes <tom@compton.nu> - 1.4.2-1
- Update to 1.4.2 upstream release

* Thu Aug  4 2016 Tom Hughes <tom@compton.nu> - 1.4.0-1
- Update to 1.4.0 upstream release

* Fri Feb 19 2016 Tom Hughes <tom@compton.nu> - 1.3.0-1
- Update to 1.3.0 upstream release
- Enable tests on ARM

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec  2 2015 Tom Hughes <tom@compton.nu> - 1.2.3-1
- Update to 1.2.3 upstream release

* Tue Nov 10 2015 Tom Hughes <tom@compton.nu> - 1.2.2-2
- BuildRequire graphviz for documentation

* Sun Oct 18 2015 Tom Hughes <tom@compton.nu> - 1.2.2-1
- Update to 1.2.2 upstream release

* Fri Oct  9 2015 Tom Hughes <tom@compton.nu> - 1.2.0-1
- Update to 1.2.0 upstream release

* Fri Sep 18 2015 Tom Hughes <tom@compton.nu> - 1.1.0-3
- Unbundle catch.hpp
- Fix warnings compiling tests

* Mon Sep  7 2015 Tom Hughes <tom@compton.nu> - 1.1.0-2
- Add description for devel package
- Build tests with correct flags

* Sat Aug 29 2015 Tom Hughes <tom@compton.nu> - 1.1.0-1
- Update to 1.1.0 upstream release

* Sat Aug 15 2015 Tom Hughes <tom@compton.nu>
- Initial build
