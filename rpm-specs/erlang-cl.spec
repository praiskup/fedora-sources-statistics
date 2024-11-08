%global realname cl

Name:		erlang-%{realname}
Version:	1.2.4
Release:	%autorelease
Summary:	OpenCL binding for Erlang
License:	MIT
URL:		https://github.com/tonyrog/%{realname}
VCS:		git:%{url}.git
Source0:	%{url}/archive/cl-%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-cl-0001-Remove-handmade-makefile.patch
BuildRequires:	erlang-edown
BuildRequires:	erlang-rebar3
BuildRequires:	gcc
BuildRequires:	ocl-icd-devel
BuildRequires:	opencl-headers
# We have only one OpenCL runtime for tests. Unfortunately tests fails to pass
# with this one.
# BuildRequires:	pocl
# BuildRequires:	opencl-filesystem

%description
%{summary}.

%prep
%autosetup -p1 -n %{realname}-cl-%{version}

%build
%{erlang3_compile}

# FIXME we don't have a port compiler plugin for rebar3 yet
mkdir -p ./priv
gcc c_src/cl_hash.c $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/cl_hash.o
gcc c_src/cl_nif.c  $CFLAGS -fPIC -c -I%{_libdir}/erlang/usr/include -o c_src/cl_nif.o
gcc c_src/cl_hash.o c_src/cl_nif.o $LDFLAGS -shared -L%{_libdir}/erlang/usr/lib -lei -lOpenCL -o priv/cl_nif.so

%install
%{erlang3_install}

%check
# Can't pass autotests for now due to limited OpenCL support in Fedora (?)
#%%{erlang3_test}

%files
%license COPYRIGHT
%doc README examples/
%{erlang_appdir}/

%changelog
%autochangelog
