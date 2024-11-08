%global lua_pkg_name lpeg

%bcond_without compat

%if %{with compat}
%{!?lua_compat_version: %global lua_compat_version 5.1}
%{!?lua_compat_libdir: %global lua_compat_libdir %{_libdir}/lua/%{lua_compat_version}}
%{!?lua_compat_pkgdir: %global lua_compat_pkgdir %{_datadir}/lua/%{lua_compat_version}}
%{!?lua_compat_builddir: %global lua_compat_builddir %{_builddir}/compat-lua-%{name}-%{version}-%{release}}
%endif

Name:           lua-%{lua_pkg_name}
Version:        1.1.0
Release:        %autorelease
Summary:        Parsing Expression Grammars for Lua

License:        MIT
URL:            http://www.inf.puc-rio.br/~roberto/%{lua_pkg_name}/
Source0:        http://www.inf.puc-rio.br/~roberto/%{lua_pkg_name}/%{lua_pkg_name}-%{version}.tar.gz
Patch1:         0001-inject-ldflags.patch

BuildRequires:  gcc
BuildRequires:  lua-devel >= %{lua_version}
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       lua(abi) = %{lua_version}
%else
Requires:       lua >= %{lua_version}
%endif

%description
LPeg is a new pattern-matching library for Lua, based on Parsing Expression
Grammars (PEGs).

%if %{with compat}
%package -n lua%{lua_compat_version}-%{lua_pkg_name}
Summary:        Parsing Expression Grammars for Lua %{lua_compat_version}
Provides:       compat-%{name}
BuildRequires:  compat-lua-devel >= %{lua_compat_version}
BuildRequires: make
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       lua(abi) = %{lua_compat_version}
%else
Requires:       lua >= %{lua_compat_version}
%endif

%description -n lua%{lua_compat_version}-%{lua_pkg_name}
LPeg is a new pattern-matching library for Lua %{lua_compat_version}
%endif

%prep
%autosetup -n %{lua_pkg_name}-%{version}

%if %{with compat}
rm -rf %{lua_compat_builddir}
cp -a . %{lua_compat_builddir}
%endif

%build
%make_build COPT="%{optflags}" LDFLAGS="%{build_ldflags}"

%if %{with compat}
pushd %{lua_compat_builddir}
%make_build COPT="-I%{_includedir}/lua-%{lua_compat_version} %{optflags}" LDFLAGS="-L%{lua_compat_libdir} %{build_ldflags}"
popd
%endif

%install
%{__install} -d -m 0755 %{buildroot}%{lua_libdir}
%{__install} -d -m 0755 %{buildroot}%{lua_pkgdir}
%{__install} -p -m 0755 lpeg.so %{buildroot}%{lua_libdir}/lpeg.so.%{version}
%{__ln_s} lpeg.so.%{version} %{buildroot}%{lua_libdir}/lpeg.so
%{__install} -p -m 0644 re.lua %{buildroot}%{lua_pkgdir}

%if %{with compat}
pushd %{lua_compat_builddir}
%{__install} -d -m 0755 %{buildroot}%{lua_compat_libdir}
%{__install} -d -m 0755 %{buildroot}%{lua_compat_pkgdir}
%{__install} -p -m 0755 lpeg.so %{buildroot}%{lua_compat_libdir}/lpeg.so.%{version}
%{__ln_s} lpeg.so.%{version} %{buildroot}%{lua_compat_libdir}/lpeg.so
%{__install} -p -m 0644 re.lua %{buildroot}%{lua_compat_pkgdir}
popd
%endif


%check
lua test.lua

%files
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%{lua_libdir}/*
%{lua_pkgdir}/*

%if %{with compat}
%files -n lua%{lua_compat_version}-%{lua_pkg_name}
%{lua_compat_libdir}/*
%{lua_compat_pkgdir}/*
%endif


%changelog
%autochangelog
