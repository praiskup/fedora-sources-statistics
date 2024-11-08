Name:           perl-Growl-GNTP
Version:        0.21
Release:        %autorelease
Summary:        Perl implementation of GNTP Protocol (Client Part)
# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Growl-GNTP
Source:         https://cpan.metacpan.org/authors/id/M/MA/MATTN/Growl-GNTP-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl-generators
BuildRequires:  perl(Crypt::CBC) >= 2.29
BuildRequires:  perl(Data::UUID) >= 0.149
BuildRequires:  perl(Digest::MD5) >= 2.36
BuildRequires:  perl(Digest::SHA) >= 5.45
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.36
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(Module::Build::Tiny)
BuildRequires:  perl(Test::More)


%description
Growl::GNTP is Perl implementation of GNTP Protocol (Client Part).

%prep
%autosetup -p1 -n Growl-GNTP-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

find %{buildroot} -type f -name .packlist -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes README.md
%license LICENSE
%dir %{perl_vendorlib}/Growl/
%{perl_vendorlib}/Growl/GNTP.pm
%{_mandir}/man3/Growl::GNTP*

%changelog
%autochangelog
