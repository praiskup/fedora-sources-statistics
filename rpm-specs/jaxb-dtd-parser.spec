Name:           jaxb-dtd-parser
Version:        1.5.1
Release:        %autorelease
Summary:        SAX-like API for parsing XML DTDs
License:        BSD-3-Clause
URL:            https://github.com/eclipse-ee4j/jaxb-dtd-parser
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)

%description
SAX-like API for parsing XML DTDs.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
API documentation for %{name}.

%prep
%autosetup -p1 -C

pushd dtd-parser

%pom_remove_parent

%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :glassfish-copyright-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
popd

%build
pushd dtd-parser
%mvn_build
popd

%install
pushd dtd-parser
%mvn_install
popd

%files -f dtd-parser/.mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%files javadoc -f dtd-parser/.mfiles-javadoc
%license LICENSE.md NOTICE.md

%changelog
%autochangelog
