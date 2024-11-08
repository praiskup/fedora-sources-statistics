Name:           trend
Version:        1.4
Release:        %autorelease
Summary:        A General-Purpose, Efficient Trend Graph

License:        LGPL-2.1-or-later
URL:            https://www.thregr.org/wavexx/software/%{name}
Source0:        %{url}/releases/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  mesa-libGL-devel
BuildRequires:  freeglut-devel

%description
trend is a general-purpose, efficient trend graph for "live" data. Data is
read in ASCII form from a file or continuously from a FIFO and displayed in
real-time into a multi-pass trend (much like a CRT oscilloscope). trend can
be used as a rapid analysis tool for progressive or time-based data series
together with trivial scripting.

%prep
%autosetup

%build
(cd src && %make_build)

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 src/%{name} %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_docdir}/%{name}
cp -r examples %{buildroot}%{_docdir}/%{name}/
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%license AUTHORS.rst COPYING.txt
%doc NEWS.rst README.rst
%{_bindir}/%{name}
%{_docdir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
