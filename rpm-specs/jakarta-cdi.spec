%bcond_with bootstrap

Name:           jakarta-cdi
Version:        2.0.2
Release:        %autorelease
Summary:        Jakarta Contexts and Dependency Injection
License:        Apache-2.0
URL:            https://jakarta.ee/specifications/cdi/2.0/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/cdi/archive/%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(jakarta.inject:jakarta.inject-api)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif

%description
Jakarta Contexts Dependency Injection specifies a means for obtaining
objects in such a way as to maximize reusability, testability and
maintainability compared to traditional approaches such as
constructors, factories, and service locators (e.g., JNDI).

%{?javadoc_package}

%prep
%autosetup -p1 -C

%pom_remove_parent
%pom_remove_parent api
%pom_disable_module spec
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_remove_dep :jakarta.el-api api
%pom_remove_dep :jakarta.interceptor-api api
rm -rf api/src/main/java/javax/enterprise/{context/,inject/spi/,inject/se/,inject/Model.java,inject/New.java}

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%changelog
%autochangelog
