Name:           esh
Version:        0.3.2
Release:        %autorelease
Summary:        Simple templating engine based on shell

License:        MIT
URL:            https://github.com/jirutka/esh
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  /usr/bin/asciidoctor
BuildRequires:  /usr/bin/make

Requires:       /usr/bin/awk
Requires:       /usr/bin/sed

%description
esh (embedded shell) is a templating engine for evaluating shell commands
embedded in arbitrary templates. It’s like ERB (Embedded RuBy) for shell,
intended to be used for templating configuration files.

%prep
%autosetup


%build
%make_build


%install
%make_install prefix=%{_prefix}


%check
%make_build test

%files
%license LICENSE
%doc README*
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
