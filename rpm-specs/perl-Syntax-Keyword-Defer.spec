# Perform optional tests
%bcond_without perl_Syntax_Keyword_Defer_enables_optional_test

# A build cycle: perl-Syntax-Keyword-Try → perl-Syntax-Keyword-Defer
%if %{with perl_Syntax_Keyword_Defer_enables_optional_test} && !%{defined perl_bootstrap}
%define optional_tests 1
%else
%define optional_tests 0
%endif

Name:           perl-Syntax-Keyword-Defer
Version:        0.11
Release:        1%{?dist}
Summary:        Add defer block syntax to Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Syntax-Keyword-Defer
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Syntax-Keyword-Defer-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XS::Parse::Keyword::Builder) >= 0.13
# Run-time:
BuildRequires:  perl(Carp)
# lib/Syntax/Keyword/Defer.xs includes XSParseKeyword.h generated by
# XS::Parse::Keyword::Builder which loads XS::Parse::Keyword.
BuildRequires:  perl(XS::Parse::Keyword) >= 0.13
BuildRequires:  perl(XSLoader)
# Tests:
# feature since Perl 5.33.7
BuildRequires:  perl(feature)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test2::V0)
%if %{optional_tests}
# Optional tests:
BuildRequires:  perl(Future)
BuildRequires:  perl(Future::AsyncAwait) >= 0.50
BuildRequires:  perl(Syntax::Keyword::Try) >= 0.18
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
# lib/Syntax/Keyword/Defer.xs includes XSParseKeyword.h generated by
# XS::Parse::Keyword::Builder which loads XS::Parse::Keyword.
Requires:       perl(XS::Parse::Keyword) >= 0.13
%if %{defined perl_XS_Parse_Keyword_ABI}
# XS::Parse::Keyword maintains multiple ABIs whose compatibility is checked at
# run-time by S_boot_xs_parse_keyword() compiled into this package.
# The ABI is defined in XSPARSEKEYWORD_ABI_VERSION of XSParseKeyword.h
Requires:       %{perl_XS_Parse_Keyword_ABI}
%endif

%description
This Perl module provides a syntax plugin that implements a block which
executes when the containing scope has finished. The "defer" blocks are
primarily intended for cases such as resource finalization tasks that may be
conditionally required.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(feature)
%if %{optional_tests}
Requires:       perl(Future)
Requires:       perl(Future::AsyncAwait) >= 0.50
Requires:       perl(Syntax::Keyword::Try) >= 0.18
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Syntax-Keyword-Defer-%{version}
%if !%{optional_tests}
for F in t/80await+defer.t t/80defer+SKT.t t/99pod.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{\A\Q'"$F"'\E\b}' MANIFEST
done
%endif
chmod +x t/*.t

%build
perl Build.PL --installdirs=vendor --optimize="$RPM_OPT_FLAGS"
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
%if %{optional_tests}
rm %{buildroot}%{_libexecdir}/%{name}/t/99pod.t
%endif
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
./Build test

%files
%license LICENSE
%doc Changes README
%dir %{perl_vendorarch}/auto/Syntax
%dir %{perl_vendorarch}/auto/Syntax/Keyword
%{perl_vendorarch}/auto/Syntax/Keyword/Defer
%dir %{perl_vendorarch}/Syntax
%dir %{perl_vendorarch}/Syntax/Keyword
%{perl_vendorarch}/Syntax/Keyword/Defer.pm
%{_mandir}/man3/Syntax::Keyword::Defer.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Sep 02 2024 Petr Pisar <ppisar@redhat.com> - 0.11-1
- 0.11 bump

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-5
- Perl 5.40 re-rebuild of bootstrapped packages

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 22 2023 Petr Pisar <ppisar@redhat.com> - 0.10-1
- 0.10 bump

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Petr Pisar <ppisar@redhat.com> - 0.09-1
- 0.09 bump

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-4
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-3
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Petr Pisar <ppisar@redhat.com> - 0.08-1
- 0.08 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-2
- Perl 5.36 rebuild

* Mon Feb 21 2022 Petr Pisar <ppisar@redhat.com> - 0.07-1
- 0.07 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 26 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-1
- 0.06 bump

* Tue Aug 17 2021 Petr Pisar <ppisar@redhat.com> - 0.05-6
- Rebuild against perl-XS-Parse-Keyword-0.12 (bug #1994077)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Petr Pisar <ppisar@redhat.com> - 0.05-4
- Rebuild against perl-XS-Parse-Keyword-0.06 (bug #1966787)

* Tue Jun 01 2021 Petr Pisar <ppisar@redhat.com> - 0.05-3
- Rebuild against XS-Parse-Keyword-0.04 (CPAN RT#136611)

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-2
- Perl 5.34 rebuild

* Thu May 06 2021 Petr Pisar <ppisar@redhat.com> 0.05-1
- Specfile autogenerated by cpanspec 1.78.