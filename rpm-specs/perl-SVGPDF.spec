# -*- rpm-spec -*-

%global metacpan https://cpan.metacpan.org/authors/id/J/JV/JV
%global FullName SVGPDF

Name: perl-%{FullName}
Summary: SVG support for Perl PDF::API2 and similar
License: BSD-2-Clause
Version: 0.088
Release: 3%{?dist}
Source: %{metacpan}/%{FullName}-%{version}.tar.gz
Url: https://metacpan.org/release/%{FullName}

# It's all plain perl, nothing architecture dependent.
BuildArch: noarch

Requires: perl(:VERSION) >= 5.26.0

BuildRequires: make
BuildRequires: perl(:VERSION)
BuildRequires: perl(Carp)
BuildRequires: perl(Exporter)
BuildRequires: perl(ExtUtils::MakeMaker) >= 7.24
BuildRequires: perl(File::LoadLines) >= 1.044
BuildRequires: perl(File::Temp)
BuildRequires: perl(Image::Info) >= 1.42
BuildRequires: perl(List::Util)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(Math::Trig)
BuildRequires: perl(Object::Pad) >= 0.78
BuildRequires: perl(PDF::API2) >= 2.043
BuildRequires: perl(Storable)
BuildRequires: perl(Test::Exception)
BuildRequires: perl(Test::More)
BuildRequires: perl(Text::ParseWords)
BuildRequires: perl(base)
BuildRequires: perl(strict)
BuildRequires: perl(utf8)
BuildRequires: perl(warnings)
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: perl-libs

# The only module of interest for the outer world is SVGPDF.
%global __requires_exclude ^perl\\(SVGPDF::
%global __provides_exclude ^perl\\(SVGPDF::
%{?perl_default_filter}
# Can't seem to get this right...
Provides: perl(SVGPDF) = %{version}

%description
This module processes SVG data and produces one or more PDF XObjects
to be placed in a PDF document.

This module is intended to be used with PDF::Builder, PDF::API2 and
other compatible perl PDF packages.

%prep
%setup -q -n %{FullName}-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%check
make test VERBOSE=1

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%doc Changes README.md
%license LICENSE.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Aug 29 2024 Johan Vromans <jvromans@squirrel.nl> - 0.088-3
- Fix summary.

* Wed Aug 28 2024 Johan Vromans <jvromans@squirrel.nl> - 0.088-2
- Fix provides.

* Tue Aug 27 2024 Johan Vromans <jvromans@squirrel.nl> - 0.088-1
- Upgrade to upstream.
- First official Fedora build.

* Mon Jan 29 2024 Johan Vromans <jvromans@squirrel.nl> - 0.085-1
- Upgrade to upstream.

* Fri Jan 26 2024 Johan Vromans <jvromans@squirrel.nl> - 0.084-1
- Upgrade to upstream.

* Tue Dec 26 2023 Johan Vromans <jvromans@squirrel.nl> - 0.083-1
- Initial Fedora package.
