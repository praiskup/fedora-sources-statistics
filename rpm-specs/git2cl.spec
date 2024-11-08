%global commit    1d74d4c0d933fc69ed5cec838c73502584dead05
%global shortcommit %(c=%{commit}; echo ${c:0:8})

Name:           git2cl
# Version 2.0 was a tag on ref 8373c9f74993e218a08819cbcdbab3f3564bbeba in old source location
# on http://josefsson.org/git2cl/ - there are unfortuantly no tags on the new repository.
# so we stick with 2.0 for ever till there is one.
Version:        2.0
Release:        0.%{autorelease -n}.20240622git%{shortcommit}%{?dist}
Summary:        Converts git logs to GNU style ChangeLog format

License:        GPL-2.0-or-later
URL:            https://savannah.nongnu.org/projects/git2cl

Source0:        https://git.savannah.gnu.org/cgit/git2cl.git/snapshot/git2cl-%{commit}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-generators

Requires:       git

%description
A quick tool to convert git logs to GNU ChangeLog format.

The tool invokes git log internally unless you pipe a log to it. 

%prep
%autosetup -n git2cl-%{commit}

%build
# Nothing to build.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m 755 git2cl $RPM_BUILD_ROOT%{_bindir}/git2cl

%files
%{_bindir}/git2cl
%doc README COPYING

%changelog
%autochangelog
