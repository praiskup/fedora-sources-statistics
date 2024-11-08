%global cli_tool cplc

Name:           classpathless-compiler
Version:        2.3
Release:        %autorelease
Summary:        Tool for recompiling java sources with customizable class providers
License:        Apache-2.0
URL:            https://github.com/mkoncek/classpathless-compiler
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  jurand
BuildRequires:  maven-local
BuildRequires:  mvn(com.beust:jcommander)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-engine)
BuildRequires:  mvn(org.ow2.asm:asm-tree)

Requires:       beust-jcommander
Requires:       javapackages-tools

%description
Classpathless compiler (CPLC) is a compiler wrapper used for compiling java
sources with customizable class providers. This tool works differently from the
traditional java compiler in that it doesn't use provided classpath but instead
pulls dependencies using an API.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n classpathless-compiler-%{version}

%java_remove_annotations -s -n SuppressFBWarnings .

%pom_remove_dep :spotbugs-annotations

%pom_remove_plugin :maven-assembly-plugin impl
%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :spotbugs-maven-plugin

%build
%mvn_build

%install
%mvn_install

%jpackage_script io.github.mkoncek.classpathless.Tool "" "" classpathless-compiler/classpathless-compiler:classpathless-compiler/classpathless-compiler-api:classpathless-compiler/classpathless-compiler-util:beust-jcommander %{cli_tool}

%files -f .mfiles
%{_bindir}/%{cli_tool}

%license LICENSE
%doc README.md

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
%autochangelog
