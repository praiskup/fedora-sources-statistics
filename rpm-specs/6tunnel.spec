Name:           6tunnel
Version:        0.13
Release:        8%{?dist}
Summary:        Tunnelling for application that don't speak IPv6

License:        GPL-2.0-only
URL:            https://github.com/wojtekka/6tunnel
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
# needed for tests
BuildRequires:  python3

# https://github.com/wojtekka/6tunnel/issues/11
# issue is closed but commit is not in a tagged release
# anything after 0.13 should have it natively
Patch:          9e4119f03f57eec67b97dddbf09d363b638791dc.patch

%description
6tunnel allows you to use services provided by IPv6 hosts with IPv4-only
applications and vice-versa. It can bind to any of your IPv4 (default) or
IPv6 addresses and forward all data to IPv4 or IPv6 (default) host.

%prep
%autosetup


%build
autoreconf -vif
%configure
%make_build


%check
%{python3} test.py


%install
%make_install


%files
%license COPYING
%doc README.md ChangeLog
%{_bindir}/6tunnel
%{_mandir}/man1/6tunnel.1*


%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 jonathanspw <jonathan@almalinux.org> - 0.13-1
- Initial package build
