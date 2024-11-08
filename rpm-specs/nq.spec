Name:           nq
Version:        1.0
Release:        %autorelease
Summary:        Unix command line queue utility

License:        CC0-1.0
URL:            https://github.com/leahneukirchen/nq
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  perl(Test::Harness)

Recommends:     (tmux or screen)

%description
The nq utility provides a very lightweight queuing system without requiring 
setup, maintenance, supervision or any long-running processes.

%prep
%autosetup

%build
%make_build CFLAGS='%{build_cflags}'

%check
%make_build check

%install
%make_install PREFIX=%{_prefix}

%files
%license COPYING
%doc README.md NEWS.md
%{_bindir}/%{name}
%{_bindir}/nqtail
%{_bindir}/nqterm
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/nqtail.1*
%{_mandir}/man1/nqterm.1*

%changelog
%autochangelog
