%global gem_name term-ansicolor

Name:           rubygem-%{gem_name}
Version:        1.11.2
Release:        %autorelease
Summary:        Ruby library that colors strings using ANSI escape sequences
License:        Apache-2.0
URL:            http://flori.github.com/term-ansicolor
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.0
BuildRequires:  rubygem(test-unit)
BuildRequires:  rubygem(tins)
BuildArch:      noarch

%description
This library uses ANSI escape sequences to control the attributes of terminal
output.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.


%package examples
Summary: Example scripts using %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description examples
Example scripts using %{name}.


%prep
%setup -q -c  -T
%gem_install -n %{SOURCE0}


%build


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Fix permissions.
find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod g-w
chmod g-w %{buildroot}%{gem_instdir}/examples/example.rb

# Remove unneeded files
# Proposed upstream at https://github.com/flori/term-ansicolor/pull/37
rm %{buildroot}%{gem_libdir}/term/ansicolor/.keep
rm %{buildroot}%{gem_cache}

%check
pushd .%{gem_instdir}
ruby -Ilib:tests -e 'Dir.glob "./tests/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/COPYING
%{gem_instdir}/bin
%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/term-ansicolor.gemspec
%{gem_instdir}/tests

%files examples 
%{_bindir}/term_cdiff
%{_bindir}/term_colortab
%{_bindir}/term_decolor
%{_bindir}/term_display
%{_bindir}/term_mandel
%{_bindir}/term_plasma
%{_bindir}/term_snow

%changelog
%autochangelog
