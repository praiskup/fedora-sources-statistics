
%global	header_dir	%{ruby_vendorarchdir}

%global	gem_name		cairo
#%%global	gem_githash	af3e3fc059

%bcond_with bootstrap
%if 0%{?fedora} >= 40
%bcond_with bootstrap
%endif

# Upstream GIT http://github.com/rcairo/

%undefine        _changelog_trimtime

Summary:	Ruby bindings for cairo
Name:		rubygem-%{gem_name}
Version:	1.17.13
Release:	6%{?dist}
# From gemspec
# SPDX confirmed
License:	GPL-2.0-or-later OR Ruby

URL:		http://cairographics.org/rcairo/
Source0:	http://rubygems.org/downloads/%{gem_name}-%{version}.gem
# Git based gem is created by below
Source1:	create-cairo-gem.sh
# FIXME
Source11:	rcairo-%{version}-test-missing-files.tar.gz
# Source11 is generated by $bash %%SOURCE12 %%version
Source12:	rcairo-create-missing-test-files.sh

Requires:	ruby(release)
BuildRequires:	ruby(release)

BuildRequires:	gcc

BuildRequires:	rubygems-devel
BuildRequires:	cairo-devel
BuildRequires:	ruby-devel
BuildRequires:	rubygem(red-colors)
# For %%check
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
BuildRequires:	rubygem(pkg-config)
BuildRequires:	rubygem(native-package-installer)
# Circular dependency
%if %{without bootstrap}
BuildRequires:	rubygem(poppler)
%endif
# Make sure at least one font is available for test/test_context.rb:57
# `initialize': out of memory (NoMemoryError)
BuildRequires:	dejavu-serif-fonts
Requires:	rubygems
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

Obsoletes:	ruby-%{gem_name} <= %{version}-%{release}
Provides:	ruby-%{gem_name} = %{version}-%{release}

%description
Ruby bindings for cairo. Cairo is a 2D graphics library with support for 
multiple output devices. Currently supported output targets include the 
X Window System, win32, and image buffers.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%package	devel
Summary:	Ruby-cairo development environment
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel
Requires:	ruby-devel
# Obsoletes / Provides
# ruby(cairo-devel) Provides is for compatibility
#
%description devel
Header files and libraries for building a extension library for the
ruby-cairo

%prep
%setup -q -n %{gem_name}-%{version}
mv ../%{gem_name}-%{version}.gemspec .

#Patches, etc

# pkg-config dependency should be for development
sed -i  %{gem_name}-%{version}.gemspec \
	-e '\@pkg-config@s|runtime_dependency|development_dependency|' \
	-e '\@native-package-installer@s|runtime_dependency|development_dependency|' \
	%{nil}

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

# Once install to TMPINSTDIR for %%check
rm -rf ./TMPINSTDIR
mkdir -p ./TMPINSTDIR/%{gem_dir}
cp -a ./%{gem_dir}/* ./TMPINSTDIR/%{gem_dir}

TOPDIR=$(pwd)

## remove all shebang, set permission to 0644
for f in $(find ./TMPINSTDIR/%{gem_instdir} -name \*.rb)
do
	sed -i -e '/^#!/d' $f
	chmod 0644 $f
done

# Move C extension
mkdir -p ./TMPINSTDIR/%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/*  TMPINSTDIR/%{gem_extdir_mri}/

pushd ./TMPINSTDIR
mkdir -p .%{header_dir}
mv .%{gem_extdir_mri}/*.h .%{header_dir}/
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}

popd

%install
cp -a ./TMPINSTDIR/* %{buildroot}/

# cleanups
rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Gemfile \
	Rakefile \
	*.gemspec \
	ext/ \
	test/ \
	%{nil}
popd

%check
export RUBYLIB=$(pwd)/TMPINSTDIR/%{gem_instdir}:$(pwd)/TMPINSTDIR/%{gem_extdir_mri}/

pushd ./TMPINSTDIR/%{gem_instdir}
# kill unneeded make process
rm -rf ./TMPBINDIR
mkdir ./TMPBINDIR
pushd ./TMPBINDIR
ln -sf /bin/true make
export PATH=$(pwd):$PATH
popd

# Install missing files
tar xf %{SOURCE11}
cp -a rcairo/test/* test

# Fix up test/run-test.rb
sed -i -e '\@require .rubygems@a\\ngem "test-unit"\n' test/run-test.rb
sed -i -e "\@require 'bundler/setup'@d" test/run-test.rb

%if %{with bootstrap}
# Kill tests which needs poppler
sed -i test/helper.rb -e '\@poppler@s@^@#@'
for f in \
	test/test_context.rb \
	test/test_pdf_surface.rb \
	%{nil}
do
	mv $f $f.orig
done
%endif

ruby ./test/run-test.rb

%files
%{gem_extdir_mri}/

%dir	%{gem_instdir}/
%doc	%{gem_instdir}/[A-CN-Z]*
%license	%{gem_instdir}/GPL

%{gem_instdir}/lib/
%{gem_spec}

%files	doc
%{gem_instdir}/samples/
%{gem_docdir}/

%files	devel
%{header_dir}/rb_cairo.h

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 06 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.13-5
- Bump and rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.13-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Tue Dec 19 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.13-1
- 1.17.13

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.12-1
- 1.17.12

* Thu Jun 15 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.9-1
- 1.17.9

* Wed May 24 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.8-5
- Enable test suite again
- SPDX migration
- spec file cleanup

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.8-3
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Thu Sep 29 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.8-2
- Once kill test suite dependency for now

* Sun Sep  4 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.8-1
- 1.17.8

* Thu Aug  4 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.7-1
- 1.17.7

* Sat Jul 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.6-1
- 1.17.6

* Thu Jul 28 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.5-6
- Modify test script for cairo 1.17.6 change

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jan 23 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.5-4
- F-36: rebuild for ruby31

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 11 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.5-1
- 1.17.5

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.6-2
- F-34: rebuild against ruby 3.0

* Thu Dec 31 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.6-1.99
- Rebuild for ruby 3.0
- Set bootstrap logic for test suite

* Sun Aug  9 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.6-1
- 1.16.6

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb  5 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.5-1
- 1.16.5

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.4-4
- Enable tests again

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.4-3
- F-32: rebuild against ruby27
- Once disable tests for circular dependency

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.2-2
- F-30: rebuild against ruby26
- Once disable tests for circular dependency

* Wed Nov 14 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.2-1
- 1.16.2

* Fri Aug 24 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.14-1
- 1.15.14

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May  2 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.13-1
- 1.15.13

* Fri Mar 16 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.12-1
- 1.15.12

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.15.11-3
- Rebuilt for switch to libxcrypt

* Wed Jan 03 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.11-2
- F-28: rebuild for ruby25

* Wed Dec 27 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.11-1
- 1.15.11

* Sat Oct 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.10-1
- 1.15.10

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Adam Jackson <ajax@redhat.com> - 1.15.9-2
- Rebuild to disable cairo-gl in F27

* Mon Jun  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.9-1
- 1.15.9

* Thu May  4 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.7-1
- 1.15.7

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.5-1
- 1.15.5

* Wed Jan 11 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.4-1
- 1.15.4

* Tue Nov 29 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.3-1
- 1.15.3

* Tue Apr 19 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.2-1
- 1.15.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.3-2
- F-24: rebuild against ruby23

* Wed Sep  9 2015 amoru TASAKA <mtasaka@fedoraproject.org> - 1.14.3-1
- 1.14.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-2
- F-22: Rebuild for ruby 2.2

* Fri Dec 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-1
- 1.14.1

* Tue Nov 25 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.0-1
- 1.14.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.9-2
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Wed Apr  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.9-1
- 1.12.9

* Mon Dec 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.8-1
- 1.12.8

* Tue Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.6-1
- 1.12.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>
- Rebuild due to wrong %%gem_extdir_mri macro (bug 927471)

* Tue Mar 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.4-1
- 1.12.4

* Sun Mar  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.3-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct  6 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.3-1
- 1.12.3

* Thu Sep  6 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.12.2-1
- Update to 1.12.2 formal

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-0.2.gitaf3e3fc059
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.12.2-0.1.gitaf3e3fc059
- Update to 1.12.1
- And use git based gem for now to avoid test failure

* Tue Apr 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.10.2-4
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.10.2-3
- F-17: rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.10.2-1
- 1.10.2
- Make dependency for pkg-config be development only again
- Change the license tag to "GPLv2 or Ruby"
- Remove defattr

* Sun Oct 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.10.1-1
- 1.10.1

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-4
- F-15 mass rebuild
- Ignore test failure for now

* Sun Oct 31 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-3
- Move C extension so that "require %%gem_name" works correctly

* Tue Oct  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-2
- Install one font at BuildRequires for test	

* Sun Sep 19 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.10.0-1
- Update to 1.10.0

* Fri Sep  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.8.5-2
- Switch to gem
- Fix license tag

* Thu Sep  2 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.8.5-1
- Update to 1.8.5

* Wed Dec 16 2009 Allisson Azevedo <allisson@gmail.com> 1.8.1-1
- Update to 1.8.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 1.8.0-2
- Rebuild

* Sun Oct  5 2008 Allisson Azevedo <allisson@gmail.com> 1.8.0-1
- Update to 1.8.0

* Tue Sep  9 2008 Allisson Azevedo <allisson@gmail.com> 1.7.0-1
- Update to 1.7.0

* Sun May 18 2008 Allisson Azevedo <allisson@gmail.com> 1.6.1-1
- Update to 1.6.1

* Mon Feb 25 2008 Allisson Azevedo <allisson@gmail.com> 1.5.1-1
- Update to 1.5.1
- Update License for GPLv2+

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0-2
- Autorebuild for GCC 4.3

* Mon Jun 11 2007 Allisson Azevedo <allisson@gmail.com> 1.5.0-1
- Update to 1.5.0

* Sun Mar 28 2007 Allisson Azevedo <allisson@gmail.com> 1.4.1-2
- Changed license for Ruby License/GPL
- Add ruby-devel for devel requires
- Changed main group for System Environment/Libraries
- Changed install for keep timestamps

* Sun Mar 26 2007 Allisson Azevedo <allisson@gmail.com> 1.4.1-1
- Initial RPM release