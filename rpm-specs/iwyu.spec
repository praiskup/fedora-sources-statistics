%global appname include-what-you-use
%global toolchain clang
%global llvmver 18.0.0

# Opt out of https://fedoraproject.org/wiki/Changes/fno-omit-frame-pointer
# https://bugzilla.redhat.com/show_bug.cgi?id=2215937
# https://github.com/include-what-you-use/include-what-you-use/issues/1264
%undefine _include_frame_pointers

Name: iwyu
Version: 0.22
Release: 2%{?dist}

License: NCSA
Summary: C/C++ source files #include analyzer based on clang
URL: https://github.com/%{appname}/%{appname}
Source0: %{url}/archive/%{version}/%{appname}-%{version}.tar.gz

BuildRequires: clang >= %{llvmver}
BuildRequires: clang-devel >= %{llvmver}
BuildRequires: libcxx-devel >= %{llvmver}
BuildRequires: llvm-devel >= %{llvmver}
BuildRequires: llvm-static >= %{llvmver}

BuildRequires: ncurses-devel
BuildRequires: python3-devel
BuildRequires: zlib-devel

BuildRequires: cmake
BuildRequires: ninja-build

Provides: %{appname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: %{appname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
"Include what you use" means this: for every symbol (type, function, variable,
or macro) that you use in foo.cc (or foo.cpp), either foo.cc or foo.h should
include a .h file that exports the declaration of that symbol. (Similarly, for
foo_test.cc, either foo_test.cc or foo.h should do the including.) Obviously
symbols defined in foo.cc itself are excluded from this requirement.

This puts us in a state where every file includes the headers it needs to
declare the symbols that it uses. When every file includes what it uses,
then it is possible to edit any file and remove unused headers, without fear
of accidentally breaking the upwards dependencies of that file. It also
becomes easy to automatically track and update dependencies in the source
code.

%prep
%autosetup -n %{appname}-%{version} -p1
sed -e "s@\${LLVM_LIBRARY_DIR}@%{_prefix}/lib@g" -i CMakeLists.txt
%py3_shebang_fix *.py

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON
%cmake_build

%install
%cmake_install

%check
%ctest --exclude-regex "(cxx.test_(badinc|ms_inline_asm)|driver.test_offload_openmp)"

%files
%doc docs/* README.md
%license LICENSE.TXT
%{_bindir}/%{appname}
%{_bindir}/fix_includes.py
%{_bindir}/iwyu_tool.py
%{_datadir}/%{appname}/
%{_mandir}/man1/%{appname}.1*

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 27 2024 Vitaly <vitaly@easycoding.org> - 0.22-1
- Updated to version 0.22.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
