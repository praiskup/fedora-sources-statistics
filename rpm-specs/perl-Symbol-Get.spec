Name:           perl-Symbol-Get
Version:        0.12
Release:        %autorelease
Summary:        Read Perl’s symbol table programmatically

License:        MIT
URL:            https://metacpan.org/dist/Symbol-Get
Source0:        https://cpan.metacpan.org/authors/id/F/FE/FELIPE/Symbol-Get-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  /usr/bin/chmod
BuildRequires:  make
BuildRequires:  perl(Call::Context)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.44
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter

%{?perl_default_filter}


%description
Occasionally I have need to reference a variable programmatically. This
module facilitates that by providing an easy, syntactic-sugar-y,
read-only interface to the symbol table.

%prep
%autosetup -n Symbol-Get-%{version}


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
%dir %{perl_vendorlib}/Symbol
%{perl_vendorlib}/Symbol/Get.pm
%{_mandir}/man3/Symbol::Get.3pm*


%changelog
%autochangelog
