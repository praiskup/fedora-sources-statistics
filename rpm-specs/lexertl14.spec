%global commit bca1359f3e168707ec663921925a1034ac8d90c8
%global snapdate 20240506

Name:           lexertl14
Summary:        The Modular Lexical Analyser Generator
Version:        0.1.0^%{snapdate}git%{sub %{commit} 1 7}
Epoch:          1
Release:        %autorelease

License:        BSL-1.0
URL:            https://github.com/BenHanson/lexertl14
Source:         %{url}/archive/%{commit}/lexertl14-%{commit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  dos2unix

# No compiled binaries are installed, so this would be empty.
%global debug_package %{nil}

%global common_description %{expand:
This is the C++14 version of lexertl. Please prefer lexertl17 wherever
possible.}

%description %{common_description}


%package devel
Summary:        %{summary}

# Header-only library:
Provides:       lexertl14-static = %{epoch}:%{version}-%{release}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Conflicts/#_compat_package_conflicts
Conflicts:      lexertl17-devel

Provides:       lexertl14-examples = %{epoch}:%{version}%{release}
Obsoletes:      lexertl14-examples < 0.1.0^20240216git7a365a2-5

%description devel %{common_description}


%prep
%autosetup -n lexertl14-%{commit} -p1

# Fix line terminations (particularly for files that may be installed)
find . -type f -exec file '{}' '+' |
  grep -E '\bCRLF\b' |
  cut -d ':' -f 1 |
  xargs -r dos2unix --keepdate


%build
%cmake -DBUILD_TESTING:BOOL=ON -DBUILD_EXAMPLES:BOOL=ON
%cmake_build

# Make a copy of the examples directory without CMakeLists.txt files, which are
# not useful without the top-level CMakeLists.txt for the project.
mkdir _cleaned
cp -rvp examples _cleaned
find _cleaned/examples -type f -name CMakeLists.txt -print -delete


%install
%cmake_install


%check
%ctest


%files devel
%license include/lexertl/licence_1_0.txt
%doc README.md
%doc _cleaned/examples/

%{_includedir}/lexertl/

%{_libdir}/cmake/lexertl/


%changelog
%autochangelog
