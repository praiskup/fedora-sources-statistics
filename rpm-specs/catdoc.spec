Name: catdoc
Version: 0.95
Release: %autorelease
Summary: A program which converts Microsoft office files to plain text
License: GPL-2.0-or-later
URL: https://www.wagner.pp.ru/~vitus/software/catdoc/
Source0: http://ftp.wagner.pp.ru/pub/catdoc/%{name}-%{version}.tar.gz
Patch0: makefilefix.patch
BuildRequires: gcc
BuildRequires: make
BuildRequires: tk
Requires: tk

%description
catdoc is program which reads one or more Microsoft word files
and outputs text, contained insinde them to standard output.
Therefore it does same work for.doc files, as unix cat
command for plain ASCII files.
It is now accompanied by xls2csv - program which converts
Excel spreadsheet into comma-separated value file,
and catppt - utility to extract textual information
from Powerpoint files

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/catdoc
%{_bindir}/catppt
%{_bindir}/wordview
%{_bindir}/xls2csv
%{_mandir}/man1/catdoc.1.*
%{_mandir}/man1/catppt.1.*
%{_mandir}/man1/wordview.1.*
%{_mandir}/man1/xls2csv.1.*
%{_datadir}/catdoc
%doc README NEWS

%changelog
%autochangelog