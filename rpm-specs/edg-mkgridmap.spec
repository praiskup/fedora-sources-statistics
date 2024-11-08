%global         forgeurl https://gitlab.cern.ch/curios/edg-mkgridmap

Name:		edg-mkgridmap
Version:	4.0.6

%global         tag v%{version}
%forgemeta

Release:	%autorelease
Summary:	A tool to build the grid map-file from VO servers
License:	Apache-2.0
Url:		%forgeurl

Source0:	%{forgesource}

BuildArch:	noarch
BuildRequires:	perl-generators
BuildRequires:  make

Requires:	perl(URI)
Requires:	perl(Net::LDAP)
Requires:	perl(Net::LDAPS)
Requires:	perl(Term::ReadKey)
Requires:	perl(IO::Socket::SSL) >= 0.90
Requires:	perl(Net::SSLeay) >= 1.16
Requires:	perl(LWP)
Requires:	perl(XML::DOM)
Requires:	perl(Date::Manip)
Requires:       perl(LWP::Protocol::https)

%description
edg-mkgridmap is a tool to build the grid map-file from VO servers,
taking into account both VO and local policies.

%prep
%forgesetup

%build

%install
make install prefix=%{buildroot}

%files
%doc AUTHORS LICENSE MAINTAINERS
%dir %{_libexecdir}/edg-mkgridmap
%{_libexecdir}/edg-mkgridmap/edg-mkgridmap.pl
%{_sbindir}/edg-mkgridmap
%{_mandir}/man5/edg-mkgridmap.conf.5*
%{_mandir}/man8/edg-mkgridmap.8*

%changelog
%autochangelog
