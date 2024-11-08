%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")

## f29+ no longer using separate sipdir for python3
%global py3_sipdir %{_datadir}/sip/PyQt4

%global __provides_exclude_from ^(%{?python3_sitearch:%{python3_sitearch}/.*\\.so|}%{_qt4_plugindir}/.*\\.so)$

%global webkit 1
%global sip_ver 4.19.12

Summary: Python bindings for Qt4
Name:    PyQt4
Version: 4.12.3
Release: %autorelease
License: GPL-3.0-only AND BSD-3-clause
URL:     http://www.riverbankcomputing.com/software/pyqt/
%if 0%{?snap:1}
Source0:  http://www.riverbankcomputing.com/static/Downloads/%{name}/PyQt-x11-gpl-%{version}%{?snap:-snapshot-%{snap}}.tar.gz
%else
Source0:  http://sourceforge.net/projects/pyqt/files/%{name}/PyQt-%{version}/%{name}_gpl_x11-%{version}.tar.gz
%endif
Source2: pyuic4.sh

## upstreamable patches
Patch1: %{name}_gpl_x11-4.12.3-ftbfs.patch

## upstream patches
# fix FTBFS on ARM
Patch60:  qreal_float_support.diff

# Fix Python 3.10 support (rhbz#1895298)
Patch61:  python310-pyobj_ascharbuf.patch

# Fix error: invalid use of undefined type 'struct _frame'
Patch62:  %{name}-4.12.3-pyframe_getback.patch

# rhel patches
Patch300: PyQt-x11-gpl-4.11-webkit.patch

# Fix new function in Python-3.13
Patch301: %{name}-fix_function_for_Python3.13.patch

BuildRequires: make
BuildRequires: chrpath
BuildRequires: findutils
BuildRequires: gcc-c++
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(QtDBus)
BuildRequires: pkgconfig(QtDeclarative)
BuildRequires: pkgconfig(QtDesigner)
BuildRequires: pkgconfig(QtGui)
BuildRequires: pkgconfig(QtHelp)
BuildRequires: pkgconfig(QtMultimedia)
BuildRequires: pkgconfig(QtNetwork)
BuildRequires: pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(QtScript)
BuildRequires: pkgconfig(QtScriptTools)
BuildRequires: pkgconfig(QtSql)
BuildRequires: pkgconfig(QtSvg)
BuildRequires: pkgconfig(QtTest)
BuildRequires: pkgconfig(QtXml)
BuildRequires: pkgconfig(QtXmlPatterns)
BuildRequires: python3-dbus
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pyqt4-sip >= %{sip_ver}
BuildRequires: python3-sip-devel >= %{sip_ver}

%description
These are Python bindings for Qt4.

%package devel
Summary: Files needed to build other bindings based on Qt4
%if 0%{?webkit}
Obsoletes: %{name}-webkit-devel < %{version}-%{release}
Provides: %{name}-webkit-devel = %{version}-%{release}
Obsoletes: PyQt4 < 4.11.4-8
%endif
Provides: python-qt4-devel = %{version}-%{release}
Provides: pyqt4-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Requires: sip-devel
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6

%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt4 classes (e.g. KDE or your own).

%package doc
Summary: PyQt4 developer documentation and examples
BuildArch: noarch
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-doc = %{version}-%{release}

%description doc
%{summary}.

# split-out arch'd subpkg, since (currently) %%_qt4_datadir = %%_qt4_libdir
%package qsci-api
Summary: Qscintilla API file support
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
%py_provides python3-qt4-qsci-api

%description qsci-api
%{summary}.

%if 0%{?webkit}
%package webkit
Summary: Python bindings for Qt4 Webkit
BuildRequires: pkgconfig(QtWebKit)
# when -webkit was split out
Obsoletes: PyQt4 < 4.11.4-8
Provides: pyqt4-webkit = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description webkit
%{summary}.

%package -n python3-%{name}-webkit
Summary: Python3 bindings for Qt4 Webkit
Obsoletes: python3-PyQt4 < 4.11.4-8
%py_provides python3-pyqt4-webkit
Requires:  python3-PyQt4 = %{version}-%{release}

%description -n python3-%{name}-webkit
%{summary}.
%endif

# The bindings are imported as "PyQt4", hence it's reasonable to name the
# Python 3 subpackage "python3-PyQt4", despite the apparent tautology
%package -n python3-%{name}
Summary: Python 3 bindings for Qt4
Requires: python3-dbus
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%{?_sip_api:Requires: python3-pyqt4-sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if 0%{?webkit}
Obsoletes: python3-PyQt4 < 4.11.4-8
%endif
Provides: python3-qt4 = %{version}-%{release}
Provides: python%{python3_version}dist(pyqt4) = %{version}

%description -n python3-%{name}
These are Python 3 bindings for Qt4.

%package -n python3-%{name}-devel
Summary: Python 3 bindings for Qt4
%if 0%{?webkit}
%py_provides python3-%{name}-webkit-devel
%endif
Provides: python3-qt4-devel = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}
Requires: python3-sip-devel
# when split happened, upgrade path
Obsoletes: python3-PyQt4-devel < 4.10.3-6

%description -n python3-%{name}-devel
Files needed to build other Python 3 bindings for C++ classes that inherit
from any of the Qt4 classes (e.g. KDE or your own).


%prep
%setup -q -n PyQt4_gpl_x11-%{version}%{?snap:-snapshot-%{snap}}

# save orig for comparison later
cp -a ./sip/QtGui/opengl_types.sip ./sip/QtGui/opengl_types.sip.orig
%patch -P 1 -p1 -b .ftbfs
%patch -P 60 -p1 -b .arm
%patch -P 61 -p1
%patch -P 62 -p1
%if ! 0%{?webkit}
%patch -P 300 -p1 -b .webkit
%endif
%patch -P 301 -p1 -b .python3.13


%build
QT4DIR=%{_qt4_prefix}
PATH=%{_qt4_bindir}:$PATH ; export PATH

mkdir %{_target_platform}-python3
pushd %{_target_platform}-python3
%{__python3} ../configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=%{_qt4_qmake} \
  --qsci-api-destdir=%{_qt4_datadir}/qsci \
  %{?py3_sipdir:--sipdir=%{py3_sipdir}} \
  --verbose \
  CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LFLAGS="%{__global_ldflags}"
%make_build
popd


%install
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{_target_platform}-python3
%if "%py3_sipdir" == "%{_datadir}/sip/PyQt4"
# copy files to old location for compat purposes temporarily
mkdir -p %{buildroot}%{_datadir}/python3-sip
cp -alf %{buildroot}%{py3_sipdir} \
        %{buildroot}%{_datadir}/python3-sip/PyQt4
%endif
mkdir %{buildroot}%{python3_sitearch}/PyQt4/__pycache__/ ||:

# likewise, remove Python 2 code from the Python 3.1 directory:
rm -rfv %{buildroot}%{python3_sitearch}/PyQt4/uic/port_v2/

# install pyuic4 wrapper
rm -fv %{buildroot}%{_bindir}/pyuic4
install -p -m755 -D %{SOURCE2} \
  %{buildroot}%{_bindir}/pyuic4
sed -i \
  -e "s|@PYTHON3@|%{__python3}|g" \
  %{buildroot}%{_bindir}/pyuic4


%check
# verify opengl_types.sip sanity
diff -u ./sip/QtGui/opengl_types.sip.orig \
        ./sip/QtGui/opengl_types.sip ||:

%files doc
%doc doc/*
%doc examples/

%files qsci-api
# avoid dep on qscintilla-python, own %%_qt4_datadir/qsci/... here for now
%dir %{_qt4_datadir}/qsci/
%dir %{_qt4_datadir}/qsci/api/
%dir %{_qt4_datadir}/qsci/api/python/
%{_qt4_datadir}/qsci/api/python/PyQt4.api

%files -n python3-%{name}
%doc NEWS README
%license LICENSE
%{python3_dbus_dir}/qt.so
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/__init__.py*
%{python3_sitearch}/PyQt4/__pycache__/
%{python3_sitearch}/PyQt4/pyqtconfig.py*
%{python3_sitearch}/PyQt4/phonon.so
%{python3_sitearch}/PyQt4/Qt.so
%{python3_sitearch}/PyQt4/QtCore.so
%{python3_sitearch}/PyQt4/QtDBus.so
%{python3_sitearch}/PyQt4/QtDeclarative.so
%{python3_sitearch}/PyQt4/QtDesigner.so
%{python3_sitearch}/PyQt4/QtGui.so
%{python3_sitearch}/PyQt4/QtHelp.so
%{python3_sitearch}/PyQt4/QtMultimedia.so
%{python3_sitearch}/PyQt4/QtNetwork.so
%{python3_sitearch}/PyQt4/QtOpenGL.so
%{python3_sitearch}/PyQt4/QtScript.so
%{python3_sitearch}/PyQt4/QtScriptTools.so
%{python3_sitearch}/PyQt4/QtSql.so
%{python3_sitearch}/PyQt4/QtSvg.so
%{python3_sitearch}/PyQt4/QtTest.so
%{python3_sitearch}/PyQt4/QtXml.so
%{python3_sitearch}/PyQt4/QtXmlPatterns.so
%{python3_sitearch}/PyQt4/uic/
%{_qt4_plugindir}/designer/*

%if 0%{?webkit}
%files -n python3-%{name}-webkit
%{python3_sitearch}/PyQt4/QtWebKit.so
%endif

%files -n python3-%{name}-devel
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{py3_sipdir}/
# compat location
%dir %{_datadir}/python3-sip/
%{_datadir}/python3-sip/PyQt4/


%changelog
%autochangelog
