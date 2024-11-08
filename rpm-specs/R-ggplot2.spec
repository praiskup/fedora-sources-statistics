%global packname ggplot2
%global packver  3.5.1
%global rlibdir  %{_datadir}/R/library

%global __suggests_exclude ^R\\((Hmisc|maptools|quantreg|sf|vdiffr)\\)

# Not available or loops.
%bcond_with suggests

Name:             R-%{packname}
Version:          %{packver}
Release:          %autorelease
Summary:          Create Elegant Data Visualisations Using the Grammar of Graphics

License:          MIT
URL:              https://CRAN.R-project.org/package=%{packname}
Source0:          https://cran.r-project.org/src/contrib/%{packname}_%{packver}.tar.gz

# Here's the R view of the dependencies world:
# Depends:
# Imports:   R-cli, R-glue, R-grDevices, R-grid, R-gtable >= 0.1.1, R-isoband, R-lifecycle > 1.0.1, R-MASS, R-mgcv, R-rlang >= 1.1.0, R-scales >= 1.2.0, R-stats, R-tibble, R-vctrs >= 0.5.0, R-withr >= 2.5.0
# Suggests:  R-covr, R-dplyr, R-ggplot2movies, R-hexbin, R-Hmisc, R-knitr, R-lattice, R-mapproj, R-maps, R-maptools, R-multcomp, R-munsell, R-nlme, R-profvis, R-quantreg, R-ragg, R-RColorBrewer, R-rgeos, R-rmarkdown, R-rpart, R-sf >= 0.7-3, R-svglite >= 1.2.0.9001, R-testthat >= 3.1.2, R-vdiffr >= 1.0.0, R-xml2
# LinkingTo:
# Enhances:

BuildArch:        noarch
BuildRequires:    R-devel
BuildRequires:    tex(latex)
BuildRequires:    R-cli
BuildRequires:    R-glue
BuildRequires:    R-grDevices
BuildRequires:    R-grid
BuildRequires:    R-gtable >= 0.1.1
BuildRequires:    R-isoband
BuildRequires:    R-lifecycle > 1.0.1
BuildRequires:    R-MASS
BuildRequires:    R-mgcv
BuildRequires:    R-rlang >= 1.1.0
BuildRequires:    R-scales >= 1.3.0
BuildRequires:    R-stats
BuildRequires:    R-tibble
BuildRequires:    R-vctrs >= 0.6.0
BuildRequires:    R-withr >= 2.5.0

BuildRequires:    R-dplyr
BuildRequires:    R-ggplot2movies
BuildRequires:    R-hexbin
BuildRequires:    R-knitr
BuildRequires:    R-lattice
BuildRequires:    R-mapproj
BuildRequires:    R-maps
BuildRequires:    R-multcomp
BuildRequires:    R-munsell
BuildRequires:    R-nlme
BuildRequires:    R-profvis
BuildRequires:    R-ragg
BuildRequires:    R-RColorBrewer
BuildRequires:    R-rmarkdown
BuildRequires:    R-rpart
BuildRequires:    R-svglite >= 1.2.0.9001
BuildRequires:    R-testthat >= 3.1.2
BuildRequires:    R-xml2
%if %{with suggests}
BuildRequires:    R-Hmisc
BuildRequires:    R-maptools
BuildRequires:    R-quantreg
BuildRequires:    R-sf >= 0.7.3
BuildRequires:    R-vdiffr >= 1.0.0
%endif

%description
A system for 'declaratively' creating graphics, based on "The Grammar of
Graphics". You provide the data, tell 'ggplot2' how to map variables to
aesthetics, what graphical primitives to use, and it takes care of the
details.


%prep
%setup -q -c -n %{packname}

pushd %{packname}
# Don't need coverage; it's not packaged either.
sed -i 's/covr, //g' DESCRIPTION
popd


%build


%install
mkdir -p %{buildroot}%{rlibdir}
%{_bindir}/R CMD INSTALL -l %{buildroot}%{rlibdir} %{packname}
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -f %{buildroot}%{rlibdir}/R.css


%check
export LANG=C.UTF-8
%if %{with suggests}
%{_bindir}/R CMD check %{packname}
%else
_R_CHECK_FORCE_SUGGESTS_=0 VDIFFR_RUN_TESTS=false %{_bindir}/R CMD check %{packname} --no-examples --no-vignettes --no-tests
%endif


%files
%dir %{rlibdir}/%{packname}
%doc %{rlibdir}/%{packname}/doc
%doc %{rlibdir}/%{packname}/html
%{rlibdir}/%{packname}/DESCRIPTION
%doc %{rlibdir}/%{packname}/NEWS.md
%doc %{rlibdir}/%{packname}/CITATION
%license %{rlibdir}/%{packname}/LICENSE
%{rlibdir}/%{packname}/INDEX
%{rlibdir}/%{packname}/NAMESPACE
%{rlibdir}/%{packname}/Meta
%{rlibdir}/%{packname}/R
%{rlibdir}/%{packname}/help
%{rlibdir}/%{packname}/data


%changelog
%autochangelog
