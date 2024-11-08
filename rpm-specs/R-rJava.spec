%global packname rJava
%global packvers 1.0-11
%global rlibdir %{_libdir}/R/library

Name:           R-%{packname}
Version:        1.0.11
Release:        %autorelease
Summary:        Low-Level R to Java Interface

License:        LGPL-2.1-only
URL:            https://cran.r-project.org/package=%{packname}
Source0:        %{url}&version=%{packvers}#/%{packname}_%{packvers}.tar.gz

BuildRequires:  R-devel >= 3.6.0
Obsoletes:      %{name}-javadoc < %{version}-%{release}
ExclusiveArch:  %{java_arches}

%description
Low-level interface to Java VM very much like .C/.Call and friends.
Allows creation of objects, calling methods and accessing fields.

%prep
%setup -q -c -n %{packname}
rm %{packname}/inst/jri/*.jar

%build
# rebuild jars
find %{packname}/jri/REngine -name Makefile -exec sed -i 's/1.6/1.8/g' {} \;
%make_build -C %{packname}/jri/REngine
%make_build -C %{packname}/jri/REngine/JRI
mv %{packname}/jri/REngine/{REngine,JRI/JRIEngine}.jar %{packname}/inst/jri/

%install
mkdir -p %{buildroot}%{rlibdir}
%{_bindir}/R CMD INSTALL -l %{buildroot}%{rlibdir} %{packname}
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -f %{buildroot}%{rlibdir}/R.css


%check
export LANG=C.UTF-8
export _R_CHECK_FORCE_SUGGESTS_=0
%{_bindir}/R CMD check --no-manual --ignore-vignettes --no-examples %{packname}

%files
%dir %{rlibdir}/%{packname}
%doc %{rlibdir}/%{packname}/html
%doc %{rlibdir}/%{packname}/NEWS
%{rlibdir}/%{packname}/INDEX
%{rlibdir}/%{packname}/NAMESPACE
%{rlibdir}/%{packname}/DESCRIPTION
%{rlibdir}/%{packname}/Meta
%{rlibdir}/%{packname}/R
%{rlibdir}/%{packname}/help
%{rlibdir}/%{packname}/libs
%{rlibdir}/%{packname}/java
%{rlibdir}/%{packname}/jri

%changelog
%autochangelog
