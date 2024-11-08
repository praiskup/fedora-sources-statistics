Name:           perl-Module-Build-WithXSpp
Version:        0.14
Release:        %autorelease
Summary:        XS++ enhanced flavor of Module::Build
# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-Build-WithXSpp
Source:         https://cpan.metacpan.org/authors/id/S/SM/SMUELLER/Module-Build-WithXSpp-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::CppGuess) >= 0.04
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build) >= 0.26
BuildRequires:  perl(Test::More)

Requires:       perl(ExtUtils::CppGuess) >= 0.04
Requires:       perl(ExtUtils::ParseXS) >= 2.2205
Requires:       perl(ExtUtils::Typemaps) >= 1.00
Requires:       perl(ExtUtils::XSpp) >= 0.11
Requires:       perl(File::Basename)
Requires:       perl(File::Spec)
Requires:       perl(Module::Build) >= 0.26

# Filtering unversioned requires
%global __requires_exclude ^perl\\((Module::Build|ExtUtils::CppGuess)\\)$

%description
This subclass of Module::Build adds some tools and processes to make it
easier to use for wrapping C++ using XS++ (ExtUtils::XSpp).

%prep
%autosetup -p1 -n Module-Build-WithXSpp-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0

%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes README
%dir %{perl_vendorlib}/Module/
%dir %{perl_vendorlib}/Module/Build/
%{perl_vendorlib}/Module/Build/WithXSpp.pm
%{_mandir}/man3/Module::Build::WithXSpp*

%changelog
%autochangelog
