Name:           emacs-filesystem
Epoch:          1
Version:        30.0
Release:        %autorelease
Summary:        Emacs filesystem layout
URL:            https://www.gnu.org/software/emacs/
License:        CC0-1.0
BuildArch:      noarch


%description
This package provides some directories which are required by other
packages that add functionality to Emacs.


%install
install -m 0755 -d %{buildroot}%{_datadir}/emacs \
                   %{buildroot}%{_datadir}/emacs/site-lisp \
                   %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d


%files
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%dir %{_datadir}/emacs/site-lisp/site-start.d



%changelog
%autochangelog
