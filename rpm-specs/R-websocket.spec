%global packname websocket
%global rlibdir  %{_libdir}/R/library

Name:             R-%{packname}
Version:          1.4.2
Release:          %autorelease
Summary:          'WebSocket' Client Library

License:          GPL-2.0-only
URL:              https://CRAN.R-project.org/package=%{packname}
Source:           https://cran.r-project.org/src/contrib/%{packname}_%{version}.tar.gz
# Unbundle websocketpp https://github.com/rstudio/websocket/issues/59
Patch:            0001-Unbundle-websocketpp.patch
# https://github.com/rstudio/websocket/issues/111
Patch:            0002-Remove-unused-OpenSSL-engine-include-header.patch

# Here's the R view of the dependencies world:
# Depends:
# Imports:   R-R6, R-later >= 1.2.0
# Suggests:  R-httpuv, R-testthat, R-knitr, R-rmarkdown
# LinkingTo: R-cpp11, R-AsioHeaders, R-later
# Enhances:

BuildRequires:    R-devel
BuildRequires:    tex(latex)
BuildRequires:    R-R6
BuildRequires:    R-later-devel >= 1.2.0
BuildRequires:    R-httpuv
BuildRequires:    R-testthat
BuildRequires:    R-knitr
BuildRequires:    R-rmarkdown
BuildRequires:    R-cpp11-devel
BuildRequires:    R-AsioHeaders-devel
BuildRequires:    pkgconfig(openssl) >= 1.0.2
BuildRequires:    pkgconfig(websocketpp) >= 0.8.2

%description
Provides a WebSocket client interface for R. WebSocket is a protocol for
low-overhead real-time communication:
<https://en.wikipedia.org/wiki/WebSocket>.


%prep
%setup -q -c -n %{packname}

pushd %{packname}
%autopatch -p1
popd


%build


%install
mkdir -p %{buildroot}%{rlibdir}
%{_bindir}/R CMD INSTALL -l %{buildroot}%{rlibdir} %{packname}
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -f %{buildroot}%{rlibdir}/R.css


%check
# i686 segfaults?
%ifnarch i686
%{_bindir}/R CMD check %{packname}
%endif


%files
%dir %{rlibdir}/%{packname}
%doc %{rlibdir}/%{packname}/doc
%doc %{rlibdir}/%{packname}/html
%{rlibdir}/%{packname}/DESCRIPTION
%doc %{rlibdir}/%{packname}/NEWS.md
%{rlibdir}/%{packname}/INDEX
%{rlibdir}/%{packname}/NAMESPACE
%{rlibdir}/%{packname}/Meta
%{rlibdir}/%{packname}/R
%{rlibdir}/%{packname}/help
%dir %{rlibdir}/%{packname}/libs
%{rlibdir}/%{packname}/libs/%{packname}.so


%changelog
%autochangelog
