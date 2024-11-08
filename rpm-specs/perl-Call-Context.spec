Name:           perl-Call-Context
Version:        0.05
Release:        %autorelease
Summary:        Sanity-check calling context

License:        MIT

URL:            https://metacpan.org/dist/Call-Context
Source0:        https://cpan.metacpan.org/authors/id/F/FE/FELIPE/Call-Context-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  /usr/bin/chmod
BuildRequires:  make
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Test::More) >= 0.44
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter

%{?perl_default_filter}


%description
If your function only expects to return a list, then a call in some
other context is, by definition, an error. The problem is that,
depending on how the function is written, it may actually do something
expected in testing, but then in production act differently.

%prep
%autosetup -n Call-Context-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build


%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%files
%license LICENSE
%doc Changes
%doc README.md
%dir %{perl_vendorlib}/Call
%{perl_vendorlib}/Call/Context.pm
%{_mandir}/man3/Call::Context.3pm*


%changelog
%autochangelog
