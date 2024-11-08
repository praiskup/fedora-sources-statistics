Name:           perl-MIME-Lite
Version:        3.033
Release:        %autorelease
Summary:        MIME::Lite - low-calorie MIME generator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MIME-Lite
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/MIME-Lite-%{version}.tar.gz
BuildArch:      noarch
BuildRequires: make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Email::Date::Format)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(lib)
BuildRequires:  perl(Mail::Address)
BuildRequires:  perl(MIME::Types) >= 1.28
BuildRequires:  perl(Net::SMTP)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# not detected by automated find-requires:
Requires:       perl(Email::Date::Format)
Requires:       perl(MIME::Types) >= 1.28

%{?perl_default_filter}

%description
MIME::Lite is intended as a simple, standalone module for generating (not 
parsing!) MIME messages... Specifically, it allows you to output a simple,
decent single- or multi-part message with text or binary attachments.  It does
not require that you have the Mail:: or MIME:: modules installed.

%prep
%setup -q -n MIME-Lite-%{version}
sed -i 's/\r//' examples/*
sed -i 's/\r//' contrib/*
sed -i 's/\r//' COPYING README
chmod a-x examples/* contrib/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +

%check
make test

%files
%doc changes.pod README examples contrib COPYING LICENSE
%exclude %{perl_vendorlib}/MIME/changes.pod
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
%autochangelog
