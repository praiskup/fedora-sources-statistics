# RPM conditionals so as to be able to dynamically produce
# slowdebug/release builds. See:
# http://rpm.org/user_doc/conditional_builds.html
#
# Examples:
#
# Produce release, fastdebug *and* slowdebug builds on x86_64 (default):
# $ rpmbuild -ba java-1.8.0-openjdk.spec
#
# Produce only release builds (no slowdebug builds) on x86_64:
# $ rpmbuild -ba java-1.8.0-openjdk.spec --without slowdebug --without fastdebug
#
# Only produce a release build on x86_64:
# $ fedpkg mockbuild --without slowdebug --without fastdebug
#
# Only produce a debug build on x86_64:
# $ fedpkg local --without release
#
# Enable fastdebug builds by default on relevant arches.
%bcond_without fastdebug
# Enable slowdebug builds by default on relevant arches.
%bcond_without slowdebug
# Enable release builds by default on relevant arches.
%bcond_without release
# Build with system libraries
%bcond_with system_libs

%if %{with system_libs}
%global system_libs 1
%global link_type system
%global jpeg_lib |libjavajpeg[.]so.*
%else
%global system_libs 0
%global link_type bundled
%global jpeg_lib |libjpeg[.]so.*
%endif

# The -g flag says to use strip -g instead of full strip on DSOs or EXEs.
# This fixes detailed NMT and other tools which need minimal debug info.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1520879
%global _find_debuginfo_opts -g

# note: parametrized macros are order-sensitive (unlike not-parametrized) even with normal macros
# also necessary when passing it as parameter to other macros. If not macro, then it is considered a switch
# see the difference between global and define:
# See https://github.com/rpm-software-management/rpm/issues/127 to comments at  "pmatilai commented on Aug 18, 2017"
# (initiated in https://bugzilla.redhat.com/show_bug.cgi?id=1482192)
%global debug_suffix_unquoted -slowdebug
%global fastdebug_suffix_unquoted -fastdebug
# quoted one for shell operations
%global debug_suffix "%{debug_suffix_unquoted}"
%global fastdebug_suffix "%{fastdebug_suffix_unquoted}"
%global normal_suffix ""

%global debug_warning This package is unoptimised with full debugging. Install only as needed and remove ASAP.
%global fastdebug_warning This package is optimised with full debugging. Install only as needed and remove ASAP.
%global debug_on unoptimised with full debugging on
%global fastdebug_on optimised with full debugging on
%global for_fastdebug for packages with debugging on and optimisation
%global for_debug for packages with debugging on and no optimisation

%if %{with release}
%global include_normal_build 1
%else
%global include_normal_build 0
%endif

%if %{include_normal_build}
%global normal_build %{normal_suffix}
%else
%global normal_build %{nil}
%endif

# We have hardcoded list of files, which  is appearing in alternatives, and in files
# in alternatives those are slaves and master, very often triplicated by man pages
# in files all masters and slaves are ghosted
# the ghosts are here to allow installation via query like `dnf install /usr/bin/java`
# you can list those files, with appropriate sections: cat *.spec | grep -e --install -e --slave -e post_ -e alternatives
# TODO - fix those hardcoded lists via single list
# Those files must *NOT* be ghosted for *slowdebug* packages
# FIXME - if you are moving jshell or jlink or similar, always modify all three sections
# you can check via headless and devels:
#    rpm -ql --noghost java-11-openjdk-headless-11.0.1.13-8.fc29.x86_64.rpm  | grep bin
# == rpm -ql           java-11-openjdk-headless-slowdebug-11.0.1.13-8.fc29.x86_64.rpm  | grep bin
# != rpm -ql           java-11-openjdk-headless-11.0.1.13-8.fc29.x86_64.rpm  | grep bin
# similarly for other %%{_jvmdir}/{jre,java} and %%{_javadocdir}/{java,java-zip}

# while JDK is a techpreview(is_system_jdk=0), some provides are turned off. Once jdk stops to be an techpreview, move it to 1
# as sytem JDK, we mean any JDK which can run whole system java stack without issues (like bytecode issues, module issues, dependencies...)
%global is_system_jdk 0

%global aarch64         aarch64 arm64 armv8
# we need to distinguish between big and little endian PPC64
%global ppc64le         ppc64le
%global ppc64be         ppc64 ppc64p7
# Set of architectures which support multiple ABIs
%global multilib_arches %{power64} sparc64 x86_64
# Set of architectures for which we build slowdebug builds
%global debug_arches    %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64}
# Set of architectures for which we build fastdebug builds
%global fastdebug_arches x86_64 ppc64le aarch64
# Set of architectures with a Just-In-Time (JIT) compiler
%global jit_arches      %{aarch64} %{ix86} %{power64} sparcv9 sparc64 x86_64
# Set of architectures which use the Zero assembler port (!jit_arches)
%global zero_arches %{arm} ppc s390 s390x riscv64
# Set of architectures which run a full bootstrap cycle
%global bootstrap_arches %{jit_arches} %{zero_arches}
# Set of architectures which support SystemTap tapsets
%global systemtap_arches %{jit_arches}
# Set of architectures which support the serviceability agent
%global sa_arches       %{ix86} x86_64 sparcv9 sparc64 %{aarch64}
# Set of architectures which support class data sharing
# See https://bugzilla.redhat.com/show_bug.cgi?id=513605
# MetaspaceShared::generate_vtable_methods is not implemented for the PPC JIT
%global share_arches    %{ix86} x86_64 sparcv9 sparc64 %{aarch64}
# Set of architectures which support Java Flight Recorder (JFR)
%global jfr_arches      %{jit_arches}
# Set of architectures for which alt-java has SSB mitigation
%global ssbd_arches x86_64
# Set of architectures where we verify backtraces with gdb
%global gdb_arches %{jit_arches} %{zero_arches}
# Set of architectures for which we have a portable build
%global portable_build_arches %{aarch64} %{ix86} %{power64} s390x x86_64

# By default, we build a debug build during main build on JIT architectures
%if %{with slowdebug}
%ifarch %{debug_arches}
%global include_debug_build 1
%else
%global include_debug_build 0
%endif
%else
%global include_debug_build 0
%endif

# By default, we build a fastdebug build during main build only on fastdebug architectures
%if %{with fastdebug}
%ifarch %{fastdebug_arches}
%global include_fastdebug_build 1
%else
%global include_fastdebug_build 0
%endif
%else
%global include_fastdebug_build 0
%endif

%if %{include_debug_build}
%global slowdebug_build %{debug_suffix}
%else
%global slowdebug_build %{nil}
%endif

%if %{include_fastdebug_build}
%global fastdebug_build %{fastdebug_suffix}
%else
%global fastdebug_build %{nil}
%endif

# If you disable all builds, then the build fails
# Build and test slowdebug first as it provides the best diagnostics
%global build_loop  %{slowdebug_build} %{fastdebug_build} %{normal_build}

# VM variant being built
%ifarch %{zero_arches}
%global vm_variant zero
%else
%global vm_variant server
%endif

# debugedit tool for rewriting ELF file paths
%global debugedit %( if [ -f "%{_rpmconfigdir}/debugedit"  ]; then echo "%{_rpmconfigdir}/debugedit" ; else echo "/usr/bin/debugedit"; fi )

# With disabled nss is NSS deactivated, so NSS_LIBDIR can contain the wrong path
# the initialization must be here. Later the pkg-config have buggy behavior
# looks like openjdk RPM specific bug
# Always set this so the nss.cfg file is not broken
%global NSS_LIBDIR %(pkg-config --variable=libdir nss)
%global NSS_LIBS %(pkg-config --libs nss)
%global NSS_CFLAGS %(pkg-config --cflags nss-softokn)
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332456
%global NSSSOFTOKN_BUILDTIME_NUMBER %(pkg-config --modversion nss-softokn || : )
%global NSS_BUILDTIME_NUMBER %(pkg-config --modversion nss || : )
# this is workaround for processing of requires during srpm creation
%global NSSSOFTOKN_BUILDTIME_VERSION %(if [ "x%{NSSSOFTOKN_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSSSOFTOKN_BUILDTIME_NUMBER}" ;fi)
%global NSS_BUILDTIME_VERSION %(if [ "x%{NSS_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSS_BUILDTIME_NUMBER}" ;fi)

# In some cases, the arch used by the JDK does
# not match _arch.
# Also, in some cases, the machine name used by SystemTap
# does not match that given by _target_cpu
%ifarch x86_64
%global archinstall amd64
%global stapinstall x86_64
%endif
%ifarch ppc
%global archinstall ppc
%global stapinstall powerpc
%endif
%ifarch %{ppc64be}
%global archinstall ppc64
%global stapinstall powerpc
%endif
%ifarch %{ppc64le}
%global archinstall ppc64le
%global stapinstall powerpc
%endif
%ifarch %{ix86}
%global archinstall i386
%global stapinstall i386
%endif
%ifarch ia64
%global archinstall ia64
%global stapinstall ia64
%endif
%ifarch s390
%global archinstall s390
%global stapinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%global stapinstall s390
%endif
%ifarch %{arm}
%global archinstall arm
%global stapinstall arm
%endif
%ifarch %{aarch64}
%global archinstall aarch64
%global stapinstall arm64
%endif
%ifarch riscv64
%global archinstall riscv64
%global stapinstall %{nil}
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%global stapinstall %{_target_cpu}
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%global stapinstall %{_target_cpu}
%endif
# Need to support noarch for srpm build
%ifarch noarch
%global archinstall %{nil}
%global stapinstall %{nil}
%endif



%ifarch %{systemtap_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# New Version-String scheme-style defines
%global featurever 8
%global majorver 8

# Define version of OpenJDK 8 used
%global project openjdk
%global repo shenandoah-jdk8u
%global openjdk_revision jdk8u432-b06
%global shenandoah_revision shenandoah-%{openjdk_revision}
# Define IcedTea version used for SystemTap tapsets and desktop files
# Define IcedTea version used for SystemTap tapsets and desktop file
%global icedteaver      3.15.0
# Define current Git revision for the cacerts patch
%global cacertsver 8139f2361c2

%ifarch %{ix86} x86_64
%global with_openjfx_binding 1
%global openjfx_path %{_jvmdir}/openjfx8
# links src directories
%global jfx_jre_libs_dir %{openjfx_path}/rt/lib
%global jfx_jre_native_dir %{jfx_jre_libs_dir}/%{archinstall}
%global jfx_sdk_libs_dir %{openjfx_path}/lib
%global jfx_sdk_bins_dir %{openjfx_path}/bin
%global jfx_jre_exts_dir %{jfx_jre_libs_dir}/ext
# links src files
# maybe depend on jfx and generate the lists in build time? Yes, bad idea to inlcude cyclic depndenci, but this list is aweful
%global jfx_jre_libs jfxswt.jar javafx.properties
%global jfx_jre_native libprism_es2.so libprism_common.so libjavafx_font.so libdecora_sse.so libjavafx_font_freetype.so libprism_sw.so libjavafx_font_pango.so libglass.so libjavafx_iio.so libglassgtk2.so libglassgtk3.so
%global jfx_sdk_libs javafx-mx.jar packager.jar ant-javafx.jar
%global jfx_sdk_bins javafxpackager javapackager
%global jfx_jre_exts jfxrt.jar
%else
%global with_openjfx_binding 0
%endif


# Standard JPackage naming and versioning defines
%global origin          openjdk
%global origin_nice     OpenJDK
%global top_level_dir_name   %{shenandoah_revision}
%global vcstag   %{shenandoah_revision}

# Settings for local security configuration
%global security_file %{top_level_dir_name}/jdk/src/share/lib/security/java.security-%{_target_os}
%global cacerts_file /etc/pki/java/cacerts

# Define vendor information used by OpenJDK
%global oj_vendor Red Hat, Inc.
%global oj_vendor_url "https://www.redhat.com/"
# Define what url should JVM offer in case of a crash report
# order may be important, epel may have rhel declared
%if 0%{?epel}
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora%20EPEL&component=%{name}&version=epel%{epel}
%else
%if 0%{?fedora}
# Does not work for rawhide, keeps the version field empty
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora&component=%{name}&version=%{fedora}
%else
%if 0%{?rhel}
%global oj_vendor_bug_url https://access.redhat.com/support/cases/
%else
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi
%endif
%endif
%endif

# e.g. aarch64-shenandoah-jdk8u212-b04-shenandoah-merge-2019-04-30 -> aarch64-shenandoah-jdk8u212-b04
%global version_tag     %(VERSION=%{shenandoah_revision}; echo ${VERSION%%-shenandoah-merge*})
# eg # jdk8u60-b27 -> jdk8u60 or # aarch64-jdk8u60-b27 -> aarch64-jdk8u60  (dont forget spec escape % by %%)
%global whole_update    %(VERSION=%{version_tag}; echo ${VERSION%%-*})
# eg  jdk8u60 -> 60 or aarch64-jdk8u60 -> 60
%global updatever       %(VERSION=%{whole_update}; echo ${VERSION##*u})
# eg jdk8u60-b27 -> b27
%global buildver        %(VERSION=%{version_tag}; echo ${VERSION##*-})
%global rpmrelease      %(echo "%autorelease" | sed 's;%{?dist};;')

# Define milestone (EA for pre-releases, GA ("fcs") for releases)
# Release will be (where N is usually a number starting at 1):
# - 0.N%%{?extraver}%%{?dist} for EA releases,
# - N%%{?extraver}{?dist} for GA releases
%global is_ga           1
%if %{is_ga}
%global milestone          fcs
%global milestone_version  %{nil}
%global extraver %{nil}
%global eaprefix %{nil}
%else
%global milestone          ea
%global milestone_version  "-ea"
%global extraver .%{milestone}
%global eaprefix 0.
%endif
# priority must be 7 digits in total; up to openjdk 1.8
%if %is_system_jdk
%global priority        1800%{updatever}
%else
# for non-default using, using 1, so slowdebugs can have 0
%global priority 0000001
%endif

%global javaver         1.%{majorver}.0

# parametrized macros are order-sensitive
%global compatiblename  %{name}
%global fullversion     %{compatiblename}-%{version}-%{release}
# output dir stub
%define installoutputdir() %{expand:install/jdk8.install%{?1}}
# we can copy the javadoc to not arched dir, or make it not noarch
%define uniquejavadocdir()    %{expand:%{fullversion}%{?1}}
# main id and dir of this jdk
%define uniquesuffix()        %{expand:%{fullversion}.%{_arch}%{?1}}

# Fix for https://bugzilla.redhat.com/show_bug.cgi?id=1111349.
# https://bugzilla.redhat.com/show_bug.cgi?id=1590796
# as to why some libraries *cannot* be excluded. In particular,
%global _privatelibs libattach[.]so.*|libawt_headless[.]so.*|libawt[.]so.*|libawt_xawt[.]so.*|libdt_socket[.]so.*|libfontmanager[.]so.*|libhprof[.]so.*|libinstrument[.]so.*|libj2gss[.]so.*|libj2pcsc[.]so.*|libj2pkcs11[.]so.*|libjaas_unix[.]so.*|libjava_crw_demo[.]so.*|libjdwp[.]so.*|libjli[.]so.*|libjsdt[.]so.*|libjsoundalsa[.]so.*|libjsound[.]so.*|liblcms[.]so.*|libmanagement[.]so.*|libmlib_image[.]so.*|libnet[.]so.*|libnio[.]so.*|libnpt[.]so.*|libsaproc[.]so.*|libsctp[.]so.*|libsplashscreen[.]so.*|libsunec[.]so.*|libsystemconf[.]so.*|libunpack[.]so.*|libzip[.]so.*|lib[.]so\\(SUNWprivate_.*%{jpeg_lib}
%global _publiclibs libjawt[.]so.*|libjava[.]so.*|libjvm[.]so.*|libverify[.]so.*|libjsig[.]so.*


%if %is_system_jdk
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$
# Never generate lib-style provides/requires for slowdebug packages
%global __provides_exclude_from ^.*/%{uniquesuffix -- %{debug_suffix_unquoted}}/.*$
%global __requires_exclude_from ^.*/%{uniquesuffix -- %{debug_suffix_unquoted}}/.*$
%global __provides_exclude_from ^.*/%{uniquesuffix -- %{fastdebug_suffix_unquoted}}/.*$
%global __requires_exclude_from ^.*/%{uniquesuffix -- %{fastdebug_suffix_unquoted}}/.*$
%else
# Don't generate provides/requires for JDK provided shared libraries at all.
%global __provides_exclude ^(%{_privatelibs}|%{_publiclibs})$
%global __requires_exclude ^(%{_privatelibs}|%{_publiclibs})$
%endif


%global etcjavasubdir     %{_sysconfdir}/java/java-%{javaver}-%{origin}
%define etcjavadir()      %{expand:%{etcjavasubdir}/%{uniquesuffix -- %{?1}}}
# Standard JPackage directories and symbolic links.
%define sdkdir()        %{expand:%{uniquesuffix -- %{?1}}}
%define jrelnk()        %{expand:jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}%{?1}}

%define jredir()        %{expand:%{sdkdir -- %{?1}}/jre}
%define sdkbindir()     %{expand:%{_jvmdir}/%{sdkdir -- %{?1}}/bin}
%define jrebindir()     %{expand:%{_jvmdir}/%{jredir -- %{?1}}/bin}
%global alt_java_name     alt-java

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/
%global repack_file repack.info

# For flatpack builds hard-code dependency paths,
# otherwise use relative paths.
%if 0%{?flatpak}
%global alternatives_requires /usr/sbin/alternatives
%global javazidir /usr/share/javazi-1.8
%global portablejvmdir /usr/lib/jvm
%else
%global alternatives_requires %{_sbindir}/alternatives
%global javazidir %{_datadir}/javazi-1.8
%global portablejvmdir %{_jvmdir}
%endif

%global family %{name}.%{_arch}
%global family_noarch  %{name}

%if %{with_systemtap}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific sub-dir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinguish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka target_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdirttapset %{tapsetroot}/tapset/
%global tapsetdir %{tapsetdirttapset}/%{stapinstall}
%endif

# x86 is no longer supported
%if 0%{?java_arches:1}
ExclusiveArch:  %{java_arches}
%else
ExcludeArch: %{ix86}
%endif

# not-duplicated scriptlets for normal/debug packages
%global update_desktop_icons /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%define save_alternatives() %{expand:
  # warning! alternatives are localised!
  # LANG=cs_CZ.UTF-8  alternatives --display java | head
  # LANG=en_US.UTF-8  alternatives --display java | head
  function nonLocalisedAlternativesDisplayOfMaster() {
    LANG=en_US.UTF-8 alternatives --display "$MASTER"
  }
  function headOfAbove() {
    nonLocalisedAlternativesDisplayOfMaster | head -n $1
  }
  MASTER="%{?1}"
  LOCAL_LINK="%{?2}"
  FAMILY="%{?3}"
  rm -f %{_localstatedir}/lib/rpm-state/"$MASTER"_$FAMILY > /dev/null
  if nonLocalisedAlternativesDisplayOfMaster > /dev/null ; then
      if headOfAbove 1 | grep -q manual ; then
        if headOfAbove 2 | tail -n 1 | grep -q %{compatiblename} ; then
           headOfAbove 2  > %{_localstatedir}/lib/rpm-state/"$MASTER"_"$FAMILY"
        fi
      fi
  fi
}

%define save_and_remove_alternatives() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  upgrade1_uninstal0=%{?3}
  if [ "0$upgrade1_uninstal0" -gt 0 ] ; then # removal of this condition will cause persistence between uninstall
    %{save_alternatives %{?1} %{?2} %{?4}}
  fi
  alternatives --remove  "%{?1}" "%{?2}"
}

%define set_if_needed_alternatives() %{expand:
  MASTER="%{?1}"
  FAMILY="%{?2}"
  ALTERNATIVES_FILE="%{_localstatedir}/lib/rpm-state/$MASTER"_"$FAMILY"
  if [ -e  "$ALTERNATIVES_FILE" ] ; then
    rm "$ALTERNATIVES_FILE"
    alternatives --set $MASTER $FAMILY
  fi
}


%define post_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0
}

%define alternatives_java_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

ext=.gz
key=java
alternatives \\
  --install %{_bindir}/java $key %{jrebindir -- %{?1}}/java $PRIORITY  --family %{family} \\
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jredir -- %{?1}} \\
  --slave %{_bindir}/%{alt_java_name} %{alt_java_name} %{jrebindir -- %{?1}}/%{alt_java_name} \\
  --slave %{_bindir}/jjs jjs %{jrebindir -- %{?1}}/jjs \\
  --slave %{_bindir}/keytool keytool %{jrebindir -- %{?1}}/keytool \\
  --slave %{_bindir}/orbd orbd %{jrebindir -- %{?1}}/orbd \\
  --slave %{_bindir}/pack200 pack200 %{jrebindir -- %{?1}}/pack200 \\
  --slave %{_bindir}/rmid rmid %{jrebindir -- %{?1}}/rmid \\
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir -- %{?1}}/rmiregistry \\
  --slave %{_bindir}/servertool servertool %{jrebindir -- %{?1}}/servertool \\
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir -- %{?1}}/tnameserv \\
  --slave %{_bindir}/policytool policytool %{jrebindir -- %{?1}}/policytool \\
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir -- %{?1}}/unpack200 \\
  --slave %{_mandir}/man1/java.1$ext java.1$ext \\
  %{_mandir}/man1/java-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/%{alt_java_name}.1$ext %{alt_java_name}.1$ext \\
  %{_mandir}/man1/%{alt_java_name}-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jjs.1$ext jjs.1$ext \\
  %{_mandir}/man1/jjs-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \\
  %{_mandir}/man1/keytool-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \\
  %{_mandir}/man1/orbd-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \\
  %{_mandir}/man1/pack200-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \\
  %{_mandir}/man1/rmid-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \\
  %{_mandir}/man1/rmiregistry-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \\
  %{_mandir}/man1/servertool-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \\
  %{_mandir}/man1/tnameserv-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \\
  %{_mandir}/man1/policytool-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \\
  %{_mandir}/man1/unpack200-%{uniquesuffix -- %{?1}}.1$ext

%{set_if_needed_alternatives $key %{family}}

for X in %{origin} %{javaver} ; do
  key=jre_"$X"
  alternatives --install %{_jvmdir}/jre-"$X" $key %{_jvmdir}/%{jredir -- %{?1}} $PRIORITY --family %{family}
  %{set_if_needed_alternatives $key %{family}}
done

key=jre_%{javaver}_%{origin}
alternatives --install %{_jvmdir}/jre-%{javaver}-%{origin} $key %{_jvmdir}/%{jrelnk -- %{?1}} $PRIORITY  --family %{family}
%{set_if_needed_alternatives $key %{family}}
}

%define post_headless() %{expand:
%ifarch %{share_arches}
%{jrebindir -- %{?1}}/java -Xshare:dump >/dev/null 2>/dev/null
%endif

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

# see pretrans where this file is declared
# also see that pretrans is only for non-debug
if [ ! "%{?1}" == %{debug_suffix} ]; then
  if [ -f %{_libexecdir}/copy_jdk_configs_fixFiles.sh ] ; then
    sh  %{_libexecdir}/copy_jdk_configs_fixFiles.sh %{rpm_state_dir}/%{name}.%{_arch}  %{_jvmdir}/%{sdkdir -- %{?1}}
  fi
fi

exit 0
}

%define postun_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}


%define postun_headless() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  java  %{jrebindir -- %{?1}}/java $post_state %{family}}
  %{save_and_remove_alternatives  jre_%{origin} %{_jvmdir}/%{jredir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  jre_%{javaver} %{_jvmdir}/%{jredir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk -- %{?1}} $post_state %{family}}
}

%define posttrans_script() %{expand:
%{update_desktop_icons}
}


%define alternatives_javac_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

ext=.gz
key=javac
alternatives \\
  --install %{_bindir}/javac $key %{sdkbindir -- %{?1}}/javac $PRIORITY  --family %{family} \\
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir -- %{?1}} \\
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir -- %{?1}}/appletviewer \\
  --slave %{_bindir}/clhsdb clhsdb %{sdkbindir -- %{?1}}/clhsdb \\
  --slave %{_bindir}/extcheck extcheck %{sdkbindir -- %{?1}}/extcheck \\
  --slave %{_bindir}/hsdb hsdb %{sdkbindir -- %{?1}}/hsdb \\
  --slave %{_bindir}/idlj idlj %{sdkbindir -- %{?1}}/idlj \\
  --slave %{_bindir}/jar jar %{sdkbindir -- %{?1}}/jar \\
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir -- %{?1}}/jarsigner \\
  --slave %{_bindir}/javadoc javadoc %{sdkbindir -- %{?1}}/javadoc \\
  --slave %{_bindir}/javah javah %{sdkbindir -- %{?1}}/javah \\
  --slave %{_bindir}/javap javap %{sdkbindir -- %{?1}}/javap \\
  --slave %{_bindir}/jcmd jcmd %{sdkbindir -- %{?1}}/jcmd \\
  --slave %{_bindir}/jconsole jconsole %{sdkbindir -- %{?1}}/jconsole \\
  --slave %{_bindir}/jdb jdb %{sdkbindir -- %{?1}}/jdb \\
  --slave %{_bindir}/jdeps jdeps %{sdkbindir -- %{?1}}/jdeps \\
%ifarch %{jfr_arches}
  --slave %{_bindir}/jfr jfr %{sdkbindir -- %{?1}}/jfr \\
%endif
  --slave %{_bindir}/jhat jhat %{sdkbindir -- %{?1}}/jhat \\
  --slave %{_bindir}/jinfo jinfo %{sdkbindir -- %{?1}}/jinfo \\
  --slave %{_bindir}/jmap jmap %{sdkbindir -- %{?1}}/jmap \\
  --slave %{_bindir}/jps jps %{sdkbindir -- %{?1}}/jps \\
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir -- %{?1}}/jrunscript \\
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir -- %{?1}}/jsadebugd \\
  --slave %{_bindir}/jstack jstack %{sdkbindir -- %{?1}}/jstack \\
  --slave %{_bindir}/jstat jstat %{sdkbindir -- %{?1}}/jstat \\
  --slave %{_bindir}/jstatd jstatd %{sdkbindir -- %{?1}}/jstatd \\
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir -- %{?1}}/native2ascii \\
  --slave %{_bindir}/rmic rmic %{sdkbindir -- %{?1}}/rmic \\
  --slave %{_bindir}/schemagen schemagen %{sdkbindir -- %{?1}}/schemagen \\
  --slave %{_bindir}/serialver serialver %{sdkbindir -- %{?1}}/serialver \\
  --slave %{_bindir}/wsgen wsgen %{sdkbindir -- %{?1}}/wsgen \\
  --slave %{_bindir}/wsimport wsimport %{sdkbindir -- %{?1}}/wsimport \\
  --slave %{_bindir}/xjc xjc %{sdkbindir -- %{?1}}/xjc \\
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \\
  %{_mandir}/man1/appletviewer-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \\
  %{_mandir}/man1/extcheck-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/idlj.1$ext idlj.1$ext \\
  %{_mandir}/man1/idlj-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \\
  %{_mandir}/man1/jar-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \\
  %{_mandir}/man1/jarsigner-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \\
  %{_mandir}/man1/javac-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \\
  %{_mandir}/man1/javadoc-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \\
  %{_mandir}/man1/javah-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \\
  %{_mandir}/man1/javap-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jcmd.1$ext jcmd.1$ext \\
  %{_mandir}/man1/jcmd-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \\
  %{_mandir}/man1/jconsole-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \\
  %{_mandir}/man1/jdb-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jdeps.1$ext jdeps.1$ext \\
  %{_mandir}/man1/jdeps-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \\
  %{_mandir}/man1/jhat-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \\
  %{_mandir}/man1/jinfo-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \\
  %{_mandir}/man1/jmap-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \\
  %{_mandir}/man1/jps-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \\
  %{_mandir}/man1/jrunscript-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \\
  %{_mandir}/man1/jsadebugd-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \\
  %{_mandir}/man1/jstack-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \\
  %{_mandir}/man1/jstat-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \\
  %{_mandir}/man1/jstatd-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \\
  %{_mandir}/man1/native2ascii-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \\
  %{_mandir}/man1/rmic-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \\
  %{_mandir}/man1/schemagen-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \\
  %{_mandir}/man1/serialver-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \\
  %{_mandir}/man1/wsgen-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \\
  %{_mandir}/man1/wsimport-%{uniquesuffix -- %{?1}}.1$ext \\
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \\
  %{_mandir}/man1/xjc-%{uniquesuffix -- %{?1}}.1$ext

%{set_if_needed_alternatives  $key %{family}}

for X in %{origin} %{javaver} ; do
  key=java_sdk_"$X"
  alternatives --install %{_jvmdir}/java-"$X" $key %{_jvmdir}/%{sdkdir -- %{?1}} $PRIORITY  --family %{family}
  %{set_if_needed_alternatives  $key %{family}}
done

key=java_sdk_%{javaver}_%{origin}
alternatives --install %{_jvmdir}/java-%{javaver}-%{origin} $key %{_jvmdir}/%{sdkdir -- %{?1}} $PRIORITY  --family %{family}
%{set_if_needed_alternatives  $key %{family}}
}

%define post_devel() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0
}

%define postun_devel() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  javac %{sdkbindir -- %{?1}}/javac $post_state %{family}}
  %{save_and_remove_alternatives  java_sdk_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  java_sdk_%{javaver} %{_jvmdir}/%{sdkdir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}} $post_state %{family}}

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}

%define posttrans_devel() %{expand:
%{alternatives_javac_install --  %{?1}}
%{update_desktop_icons}
}

%define alternatives_javadoc_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

key=javadocdir
alternatives --install %{_javadocdir}/java $key %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api $PRIORITY  --family %{family_noarch}
%{set_if_needed_alternatives  $key %{family_noarch}}
exit 0
}

%define postun_javadoc() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  javadocdir  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api $post_state %{family_noarch}}
exit 0
}

%define alternatives_javadoczip_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi
key=javadoczip
alternatives --install %{_javadocdir}/java-zip $key %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $PRIORITY  --family %{family_noarch}
%{set_if_needed_alternatives  $key %{family_noarch}}
exit 0
}

%define postun_javadoc_zip() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  javadoczip  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
  %{save_and_remove_alternatives  javadoczip_%{origin}  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
  %{save_and_remove_alternatives  javadoczip_%{javaver}  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
  %{save_and_remove_alternatives  javadoczip_%{javaver}_%{origin}  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
exit 0
}

%define files_jre() %{expand:
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}-%{origin}.png
%{_datadir}/applications/*policytool%{?1}.desktop
%{_jvmdir}/%{sdkdir -- %{?1}}/jre/lib/%{archinstall}/libjsoundalsa.so
%{_jvmdir}/%{sdkdir -- %{?1}}/jre/lib/%{archinstall}/libsplashscreen.so
%{_jvmdir}/%{sdkdir -- %{?1}}/jre/lib/%{archinstall}/libawt_xawt.so
%{_jvmdir}/%{sdkdir -- %{?1}}/jre/lib/%{archinstall}/libjawt.so
%{_jvmdir}/%{sdkdir -- %{?1}}/jre/bin/policytool
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_bindir}/policytool
%endif
%endif
}


%define files_jre_headless() %{expand:
%defattr(-,root,root,-)
%dir %{_sysconfdir}/.java/.systemPrefs
%dir %{_sysconfdir}/.java
%license %{_jvmdir}/%{jredir -- %{?1}}/ASSEMBLY_EXCEPTION
%license %{_jvmdir}/%{jredir -- %{?1}}/LICENSE
%license %{_jvmdir}/%{jredir -- %{?1}}/THIRD_PARTY_README
%doc %{_defaultdocdir}/%{uniquejavadocdir -- %{?1}}/NEWS
%{_jvmdir}/%{sdkdir -- %{?1}}/NEWS
%dir %{_jvmdir}/%{sdkdir -- %{?1}}
%{_jvmdir}/%{sdkdir -- %{?1}}/release
%{_jvmdir}/%{jrelnk -- %{?1}}
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/security
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/cacerts
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/cacerts.upstream
%dir %{_jvmdir}/%{jredir -- %{?1}}
%dir %{_jvmdir}/%{jredir -- %{?1}}/bin
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib
%{_jvmdir}/%{jredir -- %{?1}}/bin/java
%{_jvmdir}/%{jredir -- %{?1}}/bin/%{alt_java_name}
%{_jvmdir}/%{jredir -- %{?1}}/bin/jjs
%{_jvmdir}/%{jredir -- %{?1}}/bin/keytool
%{_jvmdir}/%{jredir -- %{?1}}/bin/orbd
%{_jvmdir}/%{jredir -- %{?1}}/bin/pack200
%{_jvmdir}/%{jredir -- %{?1}}/bin/rmid
%{_jvmdir}/%{jredir -- %{?1}}/bin/rmiregistry
%{_jvmdir}/%{jredir -- %{?1}}/bin/servertool
%{_jvmdir}/%{jredir -- %{?1}}/bin/tnameserv
%{_jvmdir}/%{jredir -- %{?1}}/bin/unpack200
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/security/policy/unlimited/
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/security/policy/limited/
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/security/policy/
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/policy/unlimited/US_export_policy.jar
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/policy/unlimited/local_policy.jar
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/policy/limited/US_export_policy.jar
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/policy/limited/local_policy.jar
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/java.policy
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/java.security
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/blacklisted.certs
%config(noreplace) %{etcjavadir -- %{?1}}/lib/logging.properties
%config(noreplace) %{etcjavadir -- %{?1}}/lib/calendars.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/policy/unlimited/US_export_policy.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/policy/unlimited/local_policy.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/policy/limited/US_export_policy.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/policy/limited/local_policy.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/java.policy
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/java.security
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/blacklisted.certs
%{_jvmdir}/%{jredir -- %{?1}}/lib/logging.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/calendars.properties
%{_mandir}/man1/java-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/%{alt_java_name}-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jjs-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/keytool-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/orbd-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/pack200-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/rmid-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/servertool-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/tnameserv-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/policytool-%{uniquesuffix -- %{?1}}.1*
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/nss.cfg
%{_jvmdir}/%{jredir -- %{?1}}/lib/security/nss.fips.cfg
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/nss.cfg
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/nss.fips.cfg
%ifarch %{share_arches}
%attr(444, root, root) %ghost %{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/server/classes.jsa
%attr(444, root, root) %ghost %{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/client/classes.jsa
%endif
%dir %{etcjavasubdir}
%dir %{etcjavadir -- %{?1}}
%dir %{etcjavadir -- %{?1}}/lib
%dir %{etcjavadir -- %{?1}}/lib/security
%{etcjavadir -- %{?1}}/lib/security/cacerts
%dir %{etcjavadir -- %{?1}}/lib/security/policy
%dir %{etcjavadir -- %{?1}}/lib/security/policy/limited
%dir %{etcjavadir -- %{?1}}/lib/security/policy/unlimited
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/server/
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/client/
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/jli
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/jli/libjli.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/jvm.cfg
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libattach.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libawt.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libawt_headless.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libdt_socket.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libfontmanager.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libhprof.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libinstrument.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libj2gss.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libj2pcsc.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libj2pkcs11.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjaas_unix.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjava.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjava_crw_demo.so
%if %{system_libs}
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjavajpeg.so
%else
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjpeg.so
%endif
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjdwp.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjsdt.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjsig.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libjsound.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/liblcms.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libmanagement.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libmlib_image.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libnet.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libnio.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libnpt.so
%ifarch %{sa_arches}
%ifnarch %{zero_arches}
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libsaproc.so
%endif
%endif
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libsctp.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libsunec.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libsystemconf.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libunpack.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libverify.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/%{archinstall}/libzip.so
%{_jvmdir}/%{jredir -- %{?1}}/lib/charsets.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/classlist
%{_jvmdir}/%{jredir -- %{?1}}/lib/content-types.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/currency.data
%{_jvmdir}/%{jredir -- %{?1}}/lib/flavormap.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/hijrah-config-umalqura.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/images/cursors/*
%{_jvmdir}/%{jredir -- %{?1}}/lib/jce.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/jexec
%{_jvmdir}/%{jredir -- %{?1}}/lib/jsse.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/jvm.hprof.txt
%{_jvmdir}/%{jredir -- %{?1}}/lib/meta-index
%{_jvmdir}/%{jredir -- %{?1}}/lib/net.properties
%config(noreplace) %{etcjavadir -- %{?1}}/lib/net.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/psfont.properties.ja
%{_jvmdir}/%{jredir -- %{?1}}/lib/psfontj2d.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/resources.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/rt.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/sound.properties
%{_jvmdir}/%{jredir -- %{?1}}/lib/tzdb.dat
%{_jvmdir}/%{jredir -- %{?1}}/lib/tzdb.dat.upstream
%{_jvmdir}/%{jredir -- %{?1}}/lib/management-agent.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/management/*
%{_jvmdir}/%{jredir -- %{?1}}/lib/cmm/*
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/cldrdata.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/dnsns.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/jaccess.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/localedata.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/meta-index
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/nashorn.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/sunec.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/sunjce_provider.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/sunpkcs11.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/ext/zipfs.jar
%ifarch %{jfr_arches}
%{_jvmdir}/%{jredir -- %{?1}}/lib/jfr.jar
%{_jvmdir}/%{jredir -- %{?1}}/lib/jfr/default.jfc
%{_jvmdir}/%{jredir -- %{?1}}/lib/jfr/profile.jfc
%endif

%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/images
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/images/cursors
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/management
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/cmm
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/ext
%ifarch %{jfr_arches}
%dir %{_jvmdir}/%{jredir -- %{?1}}/lib/jfr
%endif
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_bindir}/java
%ghost %{_bindir}/%{alt_java_name}
%ghost %{_jvmdir}/jre
# https://bugzilla.redhat.com/show_bug.cgi?id=1312019
%ghost %{_bindir}/jjs
%ghost %{_bindir}/keytool
%ghost %{_bindir}/orbd
%ghost %{_bindir}/pack200
%ghost %{_bindir}/rmid
%ghost %{_bindir}/rmiregistry
%ghost %{_bindir}/servertool
%ghost %{_bindir}/tnameserv
%ghost %{_bindir}/unpack200
%endif
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/%{repack_file}
}

%define files_devel() %{expand:
%defattr(-,root,root,-)
%license %{_jvmdir}/%{sdkdir -- %{?1}}/ASSEMBLY_EXCEPTION
%license %{_jvmdir}/%{sdkdir -- %{?1}}/LICENSE
%license %{_jvmdir}/%{sdkdir -- %{?1}}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/bin
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/include
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/lib
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/appletviewer
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/clhsdb
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/extcheck
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/hsdb
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/idlj
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jar
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jarsigner
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/java
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/%{alt_java_name}
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/javac
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/javadoc
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/javah
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/javap
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/java-rmi.cgi
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jcmd
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jconsole
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jdb
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jdeps
%ifarch %{jfr_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jfr
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jhat
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jinfo
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jjs
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jmap
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jps
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jrunscript
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jsadebugd
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jstack
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jstat
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jstatd
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/keytool
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/native2ascii
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/orbd
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/pack200
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/policytool
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/rmic
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/rmid
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/rmiregistry
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/schemagen
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/serialver
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/servertool
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/tnameserv
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/unpack200
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/wsgen
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/wsimport
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/xjc
%{_jvmdir}/%{sdkdir -- %{?1}}/include/*
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{archinstall}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/ct.sym
%if %{with_systemtap}
%{_jvmdir}/%{sdkdir -- %{?1}}/tapset
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/ir.idl
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jconsole.jar
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/orb.idl
%ifarch %{sa_arches}
%ifnarch %{zero_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/sa-jdi.jar
%endif
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/dt.jar
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jexec
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/tools.jar
%{_datadir}/applications/*jconsole%{?1}.desktop
%{_mandir}/man1/appletviewer-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/extcheck-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/idlj-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jar-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jarsigner-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/javac-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/javadoc-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/javah-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/javap-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jconsole-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jcmd-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jdb-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jdeps-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jhat-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jinfo-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jmap-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jps-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jsadebugd-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jstack-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jstat-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/native2ascii-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/rmic-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/schemagen-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/serialver-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/wsgen-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/wsimport-%{uniquesuffix -- %{?1}}.1*
%{_mandir}/man1/xjc-%{uniquesuffix -- %{?1}}.1*
%if %{with_systemtap}
%dir %{tapsetroot}
%dir %{tapsetdirttapset}
%dir %{tapsetdir}
%{tapsetdir}/*%{_arch}%{?1}.stp
%endif
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_jvmdir}/java
%ghost %{_jvmdir}/%{alt_java_name}
%ghost %{_bindir}/appletviewer
%ghost %{_bindir}/clhsdb
%ghost %{_bindir}/extcheck
%ghost %{_bindir}/hsdb
%ghost %{_bindir}/idlj
%ghost %{_bindir}/jar
%ghost %{_bindir}/jarsigner
%ghost %{_bindir}/java
%ghost %{_bindir}/java-rmi.cgi
%ghost %{_bindir}/javac
%ghost %{_bindir}/javadoc
%ghost %{_bindir}/javah
%ghost %{_bindir}/javap
%ghost %{_bindir}/jcmd
%ghost %{_bindir}/jconsole
%ghost %{_bindir}/jdb
%ghost %{_bindir}/jdeps
%ghost %{_bindir}/jhat
%ghost %{_bindir}/jinfo
%ghost %{_bindir}/jjs
%ghost %{_bindir}/jmap
%ghost %{_bindir}/jps
%ghost %{_bindir}/jrunscript
%ghost %{_bindir}/jsadebugd
%ghost %{_bindir}/jstack
%ghost %{_bindir}/jstat
%ghost %{_bindir}/jstatd
%ghost %{_bindir}/keytool
%ghost %{_bindir}/native2ascii
%ghost %{_bindir}/orbd
%ghost %{_bindir}/pack200
%ghost %{_bindir}/policytool
%ghost %{_bindir}/rmic
%ghost %{_bindir}/rmid
%ghost %{_bindir}/rmiregistry
%ghost %{_bindir}/schemagen
%ghost %{_bindir}/serialver
%ghost %{_bindir}/servertool
%ghost %{_bindir}/tnameserv
%ghost %{_bindir}/unpack200
%ghost %{_bindir}/wsgen
%ghost %{_bindir}/wsimport
%ghost %{_bindir}/xjc
%endif
%endif
}

%define files_demo() %{expand:
%defattr(-,root,root,-)
%license %{_jvmdir}/%{jredir -- %{?1}}/LICENSE
}

%define files_src() %{expand:
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/README.md
%{_jvmdir}/%{sdkdir -- %{?1}}/src.zip
%{_jvmdir}/%{sdkdir -- %{?1}}/full_sources
}

%define files_javadoc() %{expand:
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir -- %{?1}}
#javadoc is in jdk8 noarch, so also license file must be treated like it
%license %{_defaultlicensedir}/java-1.8.0-openjdk-javadoc
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_javadocdir}/java
%ghost %{_javadocdir}/java-%{origin}
%ghost %{_javadocdir}/java-%{javaver}
%ghost %{_javadocdir}/java-%{javaver}-%{origin}
%endif
%endif
}

%define files_javadoc_zip() %{expand:
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip
#javadoc is in jdk8 noarch, so also license file must be treated like it
%license %{_defaultlicensedir}/java-1.8.0-openjdk-javadoc-zip
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_javadocdir}/java-zip
%ghost %{_javadocdir}/java-%{origin}.zip
%ghost %{_javadocdir}/java-%{javaver}.zip
%ghost %{_javadocdir}/java-%{javaver}-%{origin}.zip
%endif
%endif
}

# not-duplicated requires/provides/obsoletes for normal/debug packages
%define java_rpo() %{expand:
Requires: fontconfig%{?_isa}
Requires: xorg-x11-fonts-Type1
# Require libXcomposite explicitly since it's only dynamically loaded
# at runtime. Fixes screenshot issues. See JDK-8150954.
Requires: libXcomposite%{?_isa}
# Requires rest of java
Requires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
# for java-X-openjdk package's desktop binding
# Where recommendations are available, recommend Gtk+ for the Swing look and feel
%if 0%{?rhel} >= 8 || 0%{?fedora} > 0
Recommends: gtk2%{?_isa}
%endif

Provides: java-%{javaver}-%{origin}%{?1} = %{epoch}:%{version}-%{release}

# Standard JPackage base provides
Provides: jre-%{javaver}%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java%{?1} = %{epoch}:%{version}-%{release}
Provides: jre%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_headless_rpo() %{expand:
# Require /etc/pki/java/cacerts
Requires: ca-certificates
# Require javapackages-filesystem for ownership of /usr/lib/jvm/ and macros
Requires: javapackages-filesystem
# 2022g required as of JDK-8297804
Requires: tzdata-java >= 2022g
# for support of kernel stream control
# libsctp.so.1 is being `dlopen`ed on demand
Requires: lksctp-tools%{?_isa}
%if ! 0%{?flatpak}
# tool to copy jdk's configs - should be Recommends only, but then only dnf/yum enforce it,
# not rpm transaction and so no configs are persisted when pure rpm -u is run. It may be
# considered as regression
Requires: copy-jdk-configs >= 4.0
OrderWithRequires: copy-jdk-configs
%endif
# for printing support
Requires: cups-libs
# for system security properties
Requires: crypto-policies
# for FIPS PKCS11 provider
Requires: nss
# Post requires alternatives to install tool alternatives
Requires(post):   %{alternatives_requires}
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{alternatives_requires}
# Where suggestions are available, recommend the sctp and pcsc libraries
# for optional support of kernel stream control and card reader
%if 0%{?rhel} >= 8 || 0%{?fedora} > 0
Suggests: lksctp-tools%{?_isa}, pcsc-lite-devel%{?_isa}
%endif

# Standard JPackage base provides
Provides: jre-%{javaver}-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-headless%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: java-headless%{?1} = %{epoch}:%{version}-%{release}
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1312019
Provides: /usr/bin/jjs

}

%define java_devel_rpo() %{expand:
# Requires base package
Requires:         %{name}%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives
Requires(post):   %{alternatives_requires}
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{alternatives_requires}

# Standard JPackage devel provides
Provides: java-sdk-%{javaver}-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk-%{javaver}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-devel%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-devel%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-%{origin}-devel%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-devel%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_demo_rpo() %{expand:
Requires: %{name}%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}

Provides: java-%{javaver}-demo%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-demo%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-demo%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{origin}-demo%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_javadoc_rpo() %{expand:
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install javadoc alternative
Requires(post):   %{alternatives_requires}
# Postun requires alternatives to uninstall javadoc alternative
Requires(postun): %{alternatives_requires}

# Standard JPackage javadoc provides
Provides: java-%{javaver}-javadoc%{?1}%{?2} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-javadoc%{?1}%{?2} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-javadoc%{?1}%{?2} = %{epoch}:%{version}-%{release}
%endif
}

%define java_src_rpo() %{expand:
Requires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}

# Standard JPackage sources provides
Provides: java-%{javaver}-src%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-src%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-src%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{origin}-src%{?1} = %{epoch}:%{version}-%{release}
%endif
}


# Prevent brp-java-repack-jars from being run
%global __jar_repack 0

%global portable_name %{name}-portable
# the version must match, but sometmes we need to more precise, so including release
%global portable_version %{version}-2

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{updatever}.%{buildver}
Release: %{?eaprefix}%{rpmrelease}%{?extraver}%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons
# and this change was brought into RHEL-4. java-1.5.0-ibm packages
# also included the epoch in their virtual provides. This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0". In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0. So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages. Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".

Epoch:   1
Summary: %{origin_nice} %{majorver} Runtime Environment
# Groups are only used up to RHEL 8 and on Fedora versions prior to F30
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

# HotSpot code is licensed under GPLv2
# JDK library code is licensed under GPLv2 with the Classpath exception
# The Apache license is used in code taken from Apache projects (primarily JAXP & JAXWS)
# DOM levels 2 & 3 and the XML digital signature schemas are licensed under the W3C Software License
# The JSR166 concurrency code is in the public domain
# The BSD and MIT licenses are used for a number of third-party libraries (see THIRD_PARTY_README)
# The OpenJDK source tree includes the JPEG library (IJG), zlib & libpng (zlib), giflib and LCMS (MIT)
# The test code includes copies of NSS under the Mozilla Public License v2.0
# The PCSClite headers are under a BSD with advertising license
# The elliptic curve cryptography (ECC) source code is licensed under the LGPLv2.1 or any later version
# Automatically converted from old format: ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib - review is highly recommended.
License:  Apache-1.1 AND Apache-2.0 AND LicenseRef-Callaway-BSD AND LicenseRef-Callaway-BSD-with-advertising AND GPL-1.0-or-later AND GPL-2.0-only AND LicenseRef-Callaway-GPLv2-with-exceptions AND IJG AND LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-MIT AND MPL-2.0 AND LicenseRef-Callaway-Public-Domain AND W3C AND Zlib
URL:      http://openjdk.java.net/

# Shenandoah HotSpot
# aarch64-port/jdk8u-shenandoah contains an integration forest of
# OpenJDK 8u, the aarch64 port and Shenandoah
# To regenerate, use:
# VERSION=%%{shenandoah_revision}
# FILE_NAME_ROOT=%%{project}-%%{repo}-${VERSION}
# REPO_ROOT=<path to checked-out repository> generate_source_tarball.sh
# where the source is obtained from http://github.com/%%{project}/%%{repo}
%global toplevel_sourcelike_dir %{project}-%{repo}-%{shenandoah_revision}

# Use 'icedtea_sync.sh' to update the following
# They are based on code contained in the IcedTea project (3.x).
# Systemtap tapsets. Zipped up to keep it small.
Source8: tapsets-icedtea-%{icedteaver}.tar.xz

# Desktop files. Adapted from IcedTea
Source9: jconsole.desktop.in
Source10: policytool.desktop.in

# Ensure we aren't using the limited crypto policy
Source13: TestCryptoLevel.java

# Ensure ECDSA is working
Source14: TestECDSA.java

# Verify system crypto (policy) can be disabled via a property
Source15: TestSecurityProperties.java

# Ensure vendor settings are correct
Source16: CheckVendor.java

# Ensure translations are available for new timezones
Source18: TestTranslations.java

# Include portable spec and instructions on how to rebuild
Source19: README.md

# Disabled in portables
Source20: repackReproduciblePolycies.sh

BuildRequires: %{portable_name}-sources >= %{portable_version}
BuildRequires: %{portable_name}-misc >= %{portable_version}
BuildRequires: %{portable_name}-docs >= %{portable_version}

# JDK8 portable do not build static-libs-* so that portion is skipped here too
%if %{include_normal_build}
BuildRequires: %{portable_name}-unstripped >= %{portable_version}
%endif
%if %{include_fastdebug_build}
BuildRequires: %{portable_name}-devel-fastdebug >= %{portable_version}
%endif
%if %{include_debug_build}
BuildRequires: %{portable_name}-devel-slowdebug >= %{portable_version}
%endif

#############################################
#
# Dependencies
#
#############################################
BuildRequires: desktop-file-utils
# elfutils only are OK for build without AOT
BuildRequires: elfutils-devel
BuildRequires: gdb
# Requirement for setting up nss.cfg and nss.fips.cfg
BuildRequires: nss-devel
# Requirement for system security property test
BuildRequires: crypto-policies
BuildRequires: pkgconfig
BuildRequires: zip
BuildRequires: unzip
# For definitions and macros like jvmdir
BuildRequires: javapackages-filesystem
# 2023c required as of JDK-8305113
BuildRequires: tzdata-java >= 2023c

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif

%if %{system_libs}
BuildRequires: giflib-devel
BuildRequires: lcms2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
%else
# Version in jdk/src/share/native/java/util/zip/zlib/zlib.h
Provides: bundled(zlib) = 1.2.13
# Version in jdk/src/share/native/sun/awt/giflib/gif_lib.h
Provides: bundled(giflib) = 5.2.1
# Version in jdk/src/share/native/sun/java2d/cmm/lcms/lcms2.h
Provides: bundled(lcms2) = 2.10.0
# Version in jdk/src/share/native/sun/awt/image/jpeg/jpeglib.h
Provides: bundled(libjpeg) = 6b
# Version in jdk/src/share/native/sun/awt/libpng/png.h
Provides: bundled(libpng) = 1.6.39
%endif

# this is always built, also during debug-only build
# when it is built in debug-only this package is just placeholder
%{java_rpo %{nil}}

# Fix upgrade path after removal of accessibility subpackage
# As main accessibility was requiring main package, main package now have to
# java-1.8.0-openjdk-accessibility-{release, slowdebug, fastdebug} < 1:1.8.0.292.b06
# otherwise update fails
Obsoletes: java-1.8.0-openjdk-accessibility < 1:1.8.0.292.b06
Obsoletes: java-1.8.0-openjdk-accessibility-slowdebug < 1:1.8.0.292.b06
Obsoletes: java-1.8.0-openjdk-accessibility-fastdebug < 1:1.8.0.292.b06

%description
The %{origin_nice} %{majorver} runtime environment.

%if %{include_debug_build}
%package slowdebug
Summary: %{origin_nice} %{majorver} Runtime Environment %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_rpo -- %{debug_suffix_unquoted}}
%description slowdebug
The %{origin_nice} %{majorver} runtime environment.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package fastdebug
Summary: %{origin_nice} %{majorver} Runtime Environment %{fastdebug_on}
Group:   Development/Languages

%{java_rpo -- %{fastdebug_suffix_unquoted}}
%description fastdebug
The %{origin_nice} %{majorver} runtime environment.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package headless
Summary: %{origin_nice} %{majorver} Headless Runtime Environment
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_headless_rpo %{nil}}

%description headless
The %{origin_nice} %{majorver} runtime environment without audio and video support.
%endif

%if %{include_debug_build}
%package headless-slowdebug
Summary: %{origin_nice} %{majorver} Runtime Environment %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_headless_rpo -- %{debug_suffix_unquoted}}

%description headless-slowdebug
The %{origin_nice} %{majorver} runtime environment without audio and video support.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package headless-fastdebug
Summary: %{origin_nice} %{majorver} Runtime Environment %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_headless_rpo -- %{fastdebug_suffix_unquoted}}

%description headless-fastdebug
The %{origin_nice} %{majorver} runtime environment without audio and video support.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package devel
Summary: %{origin_nice} %{majorver} Development Environment
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_devel_rpo %{nil}}

%description devel
The %{origin_nice} %{majorver} development tools.
%endif

%if %{include_debug_build}
%package devel-slowdebug
Summary: %{origin_nice} %{majorver} Development Environment %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_devel_rpo -- %{debug_suffix_unquoted}}

%description devel-slowdebug
The %{origin_nice} %{majorver} development tools.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package devel-fastdebug
Summary: %{origin_nice} %{majorver} Development Environment %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Tools
%endif

%{java_devel_rpo -- %{fastdebug_suffix_unquoted}}

%description devel-fastdebug
The %{origin_nice} %{majorver} development tools.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package demo
Summary: %{origin_nice} %{majorver} Demos
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_demo_rpo %{nil}}

%description demo
The %{origin_nice} %{majorver} demos.
%endif

%if %{include_debug_build}
%package demo-slowdebug
Summary: %{origin_nice} %{majorver} Demos %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_demo_rpo -- %{debug_suffix_unquoted}}

%description demo-slowdebug
The %{origin_nice} %{majorver} demos.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package demo-fastdebug
Summary: %{origin_nice} %{majorver} Demos %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_demo_rpo -- %{fastdebug_suffix_unquoted}}

%description demo-fastdebug
The %{origin_nice} %{majorver} demos.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package src
Summary: %{origin_nice} %{majorver} Source Bundle
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_src_rpo %{nil}}

%description src
The %{compatiblename}-src sub-package contains the complete %{origin_nice} %{majorver}
class library source code for use by IDE indexers and debuggers.
%endif

%if %{include_debug_build}
%package src-slowdebug
Summary: %{origin_nice} %{majorver} Source Bundle %{for_debug}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_src_rpo -- %{debug_suffix_unquoted}}

%description src-slowdebug
The %{compatiblename}-src-slowdebug sub-package contains the complete %{origin_nice} %{majorver}
 class library source code for use by IDE indexers and debuggers, %{for_debug}.
%endif

%if %{include_fastdebug_build}
%package src-fastdebug
Summary: %{origin_nice} %{majorver} Source Bundle %{for_fastdebug}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_src_rpo -- %{fastdebug_suffix_unquoted}}

%description src-fastdebug
The %{compatiblename}-src-fastdebug sub-package contains the complete %{origin_nice} %{majorver}
 class library source code for use by IDE indexers and debuggers, %{for_fastdebug}.
%endif


%if %{include_normal_build}
%package javadoc
Summary: %{origin_nice} %{majorver} API documentation
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Documentation
%endif
Requires: javapackages-filesystem
Obsoletes: javadoc-slowdebug < 1:1.8.0.222.b10-1
BuildArch: noarch

%{java_javadoc_rpo %{nil}}

%description javadoc
The %{origin_nice} %{majorver} API documentation.
%endif

%if %{include_normal_build}
%package javadoc-zip
Summary: %{origin_nice} %{majorver} API documentation compressed in a single archive
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Documentation
%endif
Requires: javapackages-filesystem
Obsoletes: javadoc-zip-slowdebug < 1:1.8.0.222.b10-1
BuildArch: noarch

%{java_javadoc_rpo %{nil}}

%description javadoc-zip
The %{origin_nice} %{majorver} API documentation compressed in a single archive.
%endif

%if %{with_openjfx_binding}
%package openjfx
Summary: OpenJDK x OpenJFX connector. This package adds symliks finishing Java FX integration to %{name}
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: openjfx8%{?_isa}
Provides: javafx  = %{epoch}:%{version}-%{release}
%description openjfx
Set of links from OpenJDK (jre) to OpenJFX

%package openjfx-devel
Summary: OpenJDK x OpenJFX connector for FX developers. This package adds symliks finishing Java FX integration to %{name}-devel
Requires: %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires: openjfx8-devel%{?_isa}
Provides: javafx-devel = %{epoch}:%{version}-%{release}
%description openjfx-devel
Set of links from OpenJDK (sdk) to OpenJFX

%if %{include_debug_build}
%package openjfx-slowdebug
Summary: OpenJDK x OpenJFX connector %{for_debug}. his package adds symliks finishing Java FX integration to %{name}-slowdebug
Requires: %{name}-slowdebug%{?_isa} = %{epoch}:%{version}-%{release}
Requires: openjfx8%{?_isa}
Provides: javafx-slowdebug = %{epoch}:%{version}-%{release}
%description openjfx-slowdebug
Set of links from OpenJDK-slowdebug (jre) to normal OpenJFX. OpenJFX do not support debug buuilds of itself

%package openjfx-devel-slowdebug
Summary: OpenJDK x OpenJFX connector for FX developers %{for_debug}. This package adds symliks finishing Java FX integration to %{name}-devel-slowdebug
Requires: %{name}-devel-slowdebug%{?_isa} = %{epoch}:%{version}-%{release}
Requires: openjfx8-devel%{?_isa}
Provides: javafx-devel-slowdebug = %{epoch}:%{version}-%{release}
%description openjfx-devel-slowdebug
Set of links from OpenJDK-slowdebug (sdk) to normal OpenJFX. OpenJFX do not support debug buuilds of itself
%endif

%if %{include_fastdebug_build}
%package openjfx-fastdebug
Summary: OpenJDK x OpenJFX connector %{for_fastdebug}. his package adds symliks finishing Java FX integration to %{name}-fastdebug
Requires: %{name}-fastdebug%{?_isa} = %{epoch}:%{version}-%{release}
Requires: openjfx8%{?_isa}
Provides: javafx-fastdebug = %{epoch}:%{version}-%{release}
%description openjfx-fastdebug
Set of links from OpenJDK-fastdebug (jre) to normal OpenJFX. OpenJFX do not support debug buuilds of itself

%package openjfx-devel-fastdebug
Summary: OpenJDK x OpenJFX connector for FX developers %{for_fastdebug}. This package adds symliks finishing Java FX integration to %{name}-devel-slowdebug
Requires: %{name}-devel-fastdebug%{?_isa} = %{epoch}:%{version}-%{release}
Requires: openjfx8-devel%{?_isa}
Provides: javafx-devel-fastdebug = %{epoch}:%{version}-%{release}
%description openjfx-devel-fastdebug
Set of links from OpenJDK-fastdebug (sdk) to normal OpenJFX. OpenJFX do not support debug buuilds of itself
%endif
%endif

%prep
if [ %{include_normal_build} -eq 0 -o  %{include_normal_build} -eq 1 ] ; then
  echo "include_normal_build is %{include_normal_build}"
else
  echo "include_normal_build is %{include_normal_build}, that is invalid. Use 1 for yes or 0 for no"
  exit 11
fi
if [ %{include_debug_build} -eq 0 -o  %{include_debug_build} -eq 1 ] ; then
  echo "include_debug_build is %{include_debug_build}"
else
  echo "include_debug_build is %{include_debug_build}, that is invalid. Use 1 for yes or 0 for no"
  exit 12
fi
if [ %{include_fastdebug_build} -eq 0 -o  %{include_fastdebug_build} -eq 1 ] ; then
  echo "include_fastdebug_build is %{include_fastdebug_build}"
else
  echo "include_fastdebug_build is %{include_fastdebug_build}, that is invalid. Use 1 for yes or 0 for no"
  exit 13
fi
if [ %{include_debug_build} -eq 0 -a  %{include_normal_build} -eq 0 -a  %{include_fastdebug_build} -eq 0 ] ; then
  echo "You have disabled all builds (normal,fastdebug,slowdebug). That is a no go."
  exit 14
fi

echo "Update version: %{updatever}"
echo "Build number: %{buildver}"
echo "Milestone: %{milestone}"
# it seems that whoever was repacking starting this spec file, dropped setup macro
# as a resutl, whole repack is counting by being directly in uncleaned BUILD dir
# to fix this will need some thingking and maybe a lot fo refactoring
%setup -q -c -n %{uniquesuffix ""} -T
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 7 ] ; then
 echo "priority must be 7 digits in total, violated"
 exit 14
fi
# For old patches
ln -s %{top_level_dir_name} jdk8
ln -s %{top_level_dir_name} openjdk

# JDK8 portable do not build static-libs-* so that portion is skipped here too
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.sources.noarch.tar.xz
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.misc.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.docs.%{_arch}.tar.xz
%if %{include_normal_build}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.unstripped.jdk.%{_arch}.tar.xz
%endif
%if %{include_fastdebug_build}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.fastdebug.jdk.%{_arch}.tar.xz
%endif
%if %{include_debug_build}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.slowdebug.jdk.%{_arch}.tar.xz
%endif

# OpenJDK patches

# print out info abot binaries used for repack. The version-less fallbacks are for development only, where can be cheated environment
echo "Those RPMs are just repacking portable tarballs extracted from portable RPMs" > %{repack_file}
echo "Usually this exact portable RPM can not be obtained via dnf install, but you can download it." >> %{repack_file}
echo "The exact info is at bottom." >> %{repack_file}
echo "All java- names and versions:" >> %{repack_file}
ls -l %{_jvmdir} >> %{repack_file}
rpm -qa | grep "java-" >> %{repack_file}
echo "Used %{compatiblename}.*portable:" >> %{repack_file}
ls -l %{_jvmdir} | grep "%{compatiblename}.*portable" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Used %{name}.*portable:" >> %{repack_file}
rpm -qa | grep "%{name}.*portable" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Used %{version}.*portable:" >> %{repack_file}
ls -l %{_jvmdir} | grep "%{version}.*portable" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Used portable.*%{version}:" >> %{repack_file}
rpm -qa | grep "portable.*%{version}" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Where this is %{fullversion}" >> %{repack_file}
portableNvr=`rpm -qa | grep %{name}-portable-misc-%{version} | sed "s/-misc-/-/" | sed "s/.%{_arch}.*//"`
if [ "x${portableNvr}" == x ] ; then
  portableNvr=`rpm -qa | grep %{name}-portable-misc- | sed "s/-misc-/-/" | sed "s/.%{_arch}.*//"`" #incorrect!"
fi
echo "Which repacked ${portableNvr}" >> %{repack_file}
echo "You can download the repacked portables from:" >> %{repack_file}
echo "https://koji.fedoraproject.org/koji/search?match=glob&type=build&terms=${portableNvr}" >> %{repack_file}
echo "`date`" >> %{repack_file}

# Extract systemtap tapsets
%if %{with_systemtap}
tar --strip-components=1 -x -I xz -f %{SOURCE8}
%if %{include_debug_build}
cp -r tapset tapset%{debug_suffix}
%endif
%if %{include_fastdebug_build}
cp -r tapset tapset%{fastdebug_suffix}
%endif

for suffix in %{build_loop} ; do
  for file in "tapset"$suffix/*.in; do
    OUTPUT_FILE=`echo $file | sed -e "s:\.stp\.in$:-%{version}-%{release}.%{_arch}.stp:g"`
    sed -e "s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir -- $suffix}/jre/lib/%{archinstall}/server/libjvm.so:g" $file > $file.1
# TODO find out which architectures other than i686 have a client vm
%ifarch %{ix86}
    sed -e "s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir -- $suffix}/jre/lib/%{archinstall}/client/libjvm.so:g" $file.1 > $OUTPUT_FILE
%else
    sed -e "/@ABS_CLIENT_LIBJVM_SO@/d" $file.1 > $OUTPUT_FILE
%endif
    sed -i -e "s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir -- $suffix}:g" $OUTPUT_FILE
    sed -i -e "s:@INSTALL_ARCH_DIR@:%{archinstall}:g" $OUTPUT_FILE
    sed -i -e "s:@prefix@:%{_jvmdir}/%{sdkdir -- $suffix}/:g" $OUTPUT_FILE
  done
done
# systemtap tapsets ends
%endif

# Prepare desktop files
# The _X_ syntax indicates variables that are replaced by make upstream
# The @X@ syntax indicates variables that are replaced by configure upstream
for suffix in %{build_loop} ; do
for file in %{SOURCE9} %{SOURCE10} ; do
    FILE=`basename $file | sed -e s:\.in$::g`
    EXT="${FILE##*.}"
    NAME="${FILE%.*}"
    OUTPUT_FILE=$NAME$suffix.$EXT
    sed    -e  "s:_SDKBINDIR_:%{sdkbindir -- $suffix}:g" $file > $OUTPUT_FILE
    sed -i -e  "s:_JREBINDIR_:%{jrebindir -- $suffix}:g" $OUTPUT_FILE
    sed -i -e  "s:@target_cpu@:%{_arch}:g" $OUTPUT_FILE
    sed -i -e  "s:@OPENJDK_VER@:%{version}-%{release}.%{_arch}$suffix:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VER@:%{javaver}:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VENDOR@:%{origin}:g" $OUTPUT_FILE
done
done

# Commented as this is not there in JDK11
# Setup security policy
#sed -i -e "s:^security.systemCACerts=.*:security.systemCACerts=%{cacerts_file}:" `find . -name "java.security-%{_target_os}"`

%build
# we need to symlink sources to expected lcoation, so debuginfo strip can locate debugsources
src_image=`ls -d %{compatiblename}*%{version}*portable.sources.noarch`
ln -s $src_image/%{vcstag} %{vcstag} # this one shpuld be enoug
# cpio is complaining baout several files from build dir. Attempt here, but seems not to be correct
# as those sources are generated during build and so it have to be fixed in portables first
mkdir build
pushd build
  ln -s ../$src_image/%{vcstag} jdk%{featurever}.build
  ln -s ../$src_image/%{vcstag} jdk%{featurever}.build-fastdebug
  ln -s ../$src_image/%{vcstag} jdk%{featurever}.build-slowdebug
popd
doc_image=`ls -d %{compatiblename}*%{version}*portable.docs.%{_arch}`
# in addition the builddir must match the builddir of the portables, including release
# be aware, even os may be different, especially with buildonce, repack everywhere
# so deducting it from installed deps
portablenvr=`ls -d %{compatiblename}*%{version}*portable*.misc.%{_arch} | sed "s/portable.*.misc.//"`
portablebuilddir=/builddir/build/BUILD
  # Fix build paths in ELF files so it looks like we built them
  for file in $(find `pwd` -type f | grep -v -e "$src_image" -e "$doc_image") ; do
      if file ${file} | grep -q 'ELF'; then
          %{debugedit} -b "${portablebuilddir}/${portablenvr}" -d "$(pwd)" -n "${file}"
      fi
  done

%install
function installjdk() {
    local imagepath=${1}

    if [ -d ${imagepath} ] ; then
        # the build (erroneously) removes read permissions from some jars
        # this is a regression in OpenJDK 7 (our compiler):
        # http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
        find ${imagepath} -iname '*.jar' -exec chmod ugo+r {} \;
        chmod ugo+r ${imagepath}/lib/ct.sym

        # remove redundant *diz and *debuginfo files
        find ${imagepath} -iname '*.diz' -exec rm -v {} \;
        find ${imagepath} -iname '*.debuginfo' -exec rm -v {} \;

        # Build screws up permissions on binaries
        # https://bugs.openjdk.java.net/browse/JDK-8173610
        find ${imagepath} -iname '*.so' -exec chmod +x {} \;
        find ${imagepath}/bin/ -exec chmod +x {} \;

        # Install nss.cfg right away as we will be using the JRE above
      	#is already there from portables
        # Install nss.fips.cfg: NSS configuration for global FIPS mode (crypto-policies)
      	#is already there from portables
      	
      	# Turn on system security properties
        sed -i -e "s:^security.useSystemPropertiesFile=.*:security.useSystemPropertiesFile=true:" \
             ${imagepath}/jre/lib/security/java.security

        # Use system-wide tzdata
        mv ${imagepath}/jre/lib/tzdb.dat{,.upstream}
        ln -sv %{javazidir}/tzdb.dat ${imagepath}/jre/lib/tzdb.dat
        
        # Rename OpenJDK cacerts database
        mv ${imagepath}/jre/lib/security/cacerts{,.upstream}
        # Install cacerts symlink needed by some apps which hard-code the path
        ln -sv %{cacerts_file} ${imagepath}/jre/lib/security

        # add alt-java man page
	#  alt-java man and bianry are here from portables. Or not?
        # Print release information
     fi
}

# Checks on debuginfo must be performed before the files are stripped
# by the RPM installation stage
function debugcheckjdk() {
    local imagepath=${1}

    if [ -d ${imagepath} ] ; then

        # Check debug symbols are present and can identify code
        find "${imagepath}" -iname '*.so' -print0 | while read -d $'\0' lib
        do
            if [ -f "$lib" ] ; then
                echo "Testing $lib for debug symbols"
                # All these tests rely on RPM failing the build if the exit code of any set
                # of piped commands is non-zero.

                # Test for .debug_* sections in the shared object. This is the main test
                # Stripped objects will not contain these
                eu-readelf -S "$lib" | grep "] .debug_"
                test $(eu-readelf -S "$lib" | grep -E "\]\ .debug_(info|abbrev)" | wc --lines) == 2

                # Test FILE symbols. These will most likely be removed by anything that
                # manipulates symbol tables because it's generally useless. So a nice test
                # that nothing has messed with symbols
                old_IFS="$IFS"
                IFS=$'\n'
                for line in $(eu-readelf -s "$lib" | grep "00000000      0 FILE    LOCAL  DEFAULT")
                do
                     # We expect to see .cpp files, except for architectures like aarch64 and
                     # s390 where we expect .o and .oS files
                     echo "$line" | grep -E "ABS ((.*/)?[-_a-zA-Z0-9]+\.(c|cc|cpp|cxx|o|oS))?$"
                done
                IFS="$old_IFS"

                # If this is the JVM, look for javaCalls.(cpp|o) in FILEs, for extra sanity checking
                if [ "`basename $lib`" = "libjvm.so" ]; then
                    eu-readelf -s "$lib" | \
                        grep -E "00000000      0 FILE    LOCAL  DEFAULT      ABS javaCalls.(cpp|o)$"
                fi

                # Test that there are no .gnu_debuglink sections pointing to another
                # debuginfo file. There shouldn't be any debuginfo files, so the link makes
                # no sense either
                eu-readelf -S "$lib" | grep 'gnu'
                    if eu-readelf -S "$lib" | grep '] .gnu_debuglink' | grep PROGBITS; then
                        echo "bad .gnu_debuglink section."
                        eu-readelf -x .gnu_debuglink "$lib"
                        false
                    fi
            fi
        done

# Make sure gdb can do a backtrace based on line numbers on libjvm.so
# javaCalls.cpp:58 should map to:
# http://hg.openjdk.java.net/jdk8u/jdk8u/hotspot/file/ff3b27e6bcc2/src/share/vm/runtime/javaCalls.cpp#l58
# Using line number 1 might cause build problems. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1539664
# https://bugzilla.redhat.com/show_bug.cgi?id=1538767
gdb -q "${imagepath}/bin/java" <<EOF | tee gdb.out
handle SIGSEGV pass nostop noprint
handle SIGILL pass nostop noprint
set breakpoint pending on
break javaCalls.cpp:58
commands 1
backtrace
quit
end
run -version
EOF

%ifarch %{gdb_arches}
grep 'JavaCallWrapper::JavaCallWrapper' gdb.out
%endif

    fi
}

for suffix in %{build_loop} ; do
  if [ "x$suffix" = "x" ] ; then
      debugbuild=""
  else
      # change -something to .something
      debugbuild=`echo $suffix  | sed "s/-/./g"`
  fi
  # Final setup on the untarred images
  # TODO revisit. jre may be complety useless to unpack and process,
  # as all the files are taken from JDK tarball ans put to packages manually.
  # jre tarball may be usefull for  checking integrity of jre and jre headless subpackages
  #for jdkjre in jdk jre ; do
  for jdkjre in jdk ; do
    buildoutputdir=`ls -d %{compatiblename}*portable${debugbuild}.${jdkjre}*`
    top_dir_abs_main_build_path=$(pwd)/${buildoutputdir}
    installjdk ${top_dir_abs_main_build_path}
    # Check debug symbols were built into the dynamic libraries
    if [ $jdkjre == jdk ] ; then
      #jdk only?
      #debug symbol check was failing for release
      if [ ! "x$debugbuild" == "x" ] ; then
         debugcheckjdk ${top_dir_abs_main_build_path}
      fi
    fi
    # Print release information
    cat ${top_dir_abs_main_build_path}/release
  done
# build cycles
done # end of release / debug cycle loop

STRIP_KEEP_SYMTAB=libjvm*

for suffix in %{build_loop} ; do
  if [ "x$suffix" = "x" ] ; then
      debugbuild=""
  else
      # change -something to .something
      debugbuild=`echo $suffix  | sed "s/-/./g"`
  fi
  buildoutputdir=`ls -d %{compatiblename}*portable${debugbuild}.jdk*`
  top_dir_abs_main_build_path=$(pwd)/${buildoutputdir}

  jdk_image=${top_dir_abs_main_build_path}
  src_image=`echo ${top_dir_abs_main_build_path} | sed "s/\.portable.*.%{_arch}/.portable.sources.noarch/"`
  docdir=`echo ${top_dir_abs_main_build_path} | sed "s/\.portable.*.%{_arch}/.portable.docs.%{_arch}/"`
  miscdir=`echo ${top_dir_abs_main_build_path} | sed "s/\.portable.*.%{_arch}/.portable.misc.%{_arch}/"`

  # Install release notes
  commondocdir=${RPM_BUILD_ROOT}%{_defaultdocdir}/%{uniquejavadocdir -- $suffix}
  install -d -m 755 ${commondocdir}
  cp -a ${top_dir_abs_main_build_path}/NEWS ${commondocdir}

  # there was bug in one jdk, which packed symlink instead of sources, using copy in misc
  # Install icons and menu entries
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    ${miscdir}/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}-%{origin}.png
done

mkdir -p $RPM_BUILD_ROOT%{_jvmdir}

cp -a ${jdk_image} $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}
cp -a ${src_image} $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources
cp %{repack_file} $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/
#JDK8 specific, bianry file in sources
rm -vf "$RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/*/test/jdk/sun/management/jmxremote/bootstrap/solaris-sparcv9/launcher"
#JDK8 specific, binary file in sources
find "$RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/" -type f -name "*.so" -exec rm -vf {} \;
find "$RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/" -type f -executable
rm -vr $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/*/jdk/test/sun/security/pkcs11/nss/lib/
rm -vr $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/*/jdk/test/sun/management/jmxremote/bootstrap/solaris-sparcv9/
rm -vr $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/*/jdk/test/java/nio/channels/spi/SelectorProvider/inheritedChannel/lib/solaris-sparcv9/
rm -vr $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/*/jdk/test/java/nio/channels/spi/SelectorProvider/inheritedChannel/lib/linux-i586/
rm -vr $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources/*/jdk/test/java/nio/channels/spi/SelectorProvider/inheritedChannel/lib/solaris-amd64/
# Install the jdk
pushd ${jdk_image}

  # Install jsa directories so we can owe them
  mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir -- $suffix}/lib/%{archinstall}/server/
  mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir -- $suffix}/lib/%{archinstall}/client/

  #Install README.md
  install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/doc
  cp -a %{_sourcedir}/README.md $RPM_BUILD_ROOT%{_defaultdocdir}/

  #Install files for noarch javadoc/javadoc-zip
  if [ "x$debugbuild" == "x" ] ; then
      #Installing manually as its for noarch
      install -d -m 755 $RPM_BUILD_ROOT%{_defaultlicensedir}/java-1.8.0-openjdk-javadoc
      cp -a jre/{ASSEMBLY_EXCEPTION,LICENSE,THIRD_PARTY_README} $RPM_BUILD_ROOT%{_defaultlicensedir}/java-1.8.0-openjdk-javadoc
      install -d -m 755 $RPM_BUILD_ROOT%{_defaultlicensedir}/java-1.8.0-openjdk-javadoc-zip
      cp -a jre/{ASSEMBLY_EXCEPTION,LICENSE,THIRD_PARTY_README} $RPM_BUILD_ROOT%{_defaultlicensedir}/java-1.8.0-openjdk-javadoc-zip
  fi

%if %{with_systemtap}

  # Install systemtap support files
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset
  # note, that uniquesuffix  is in BUILD dir in this case; the {uniquesuffix} call was added once setup was added
  cp -a $RPM_BUILD_DIR/%{uniquesuffix ""}/tapset$suffix/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset/
  pushd  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset/
   tapsetFiles=`ls *.stp`
  popd
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  for name in $tapsetFiles ; do
    targetName=`echo $name | sed "s/.stp/$suffix.stp/"`
    ln -srvf $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset/$name $RPM_BUILD_ROOT%{tapsetdir}/$targetName
  done
%endif

  # Install versioned symlinks
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir -- $suffix} %{jrelnk -- $suffix}
  popd

  # Remove javaws man page
  rm -f man/man1/javaws*

  # Install man pages
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename $manpage .1)-%{uniquesuffix -- $suffix}.1
  done

  # Remove man pages from jdk image
  rm -rf $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/man

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}
  mkdir -p sample/rmi
  if [ ! -e sample/rmi/java-rmi.cgi ] ; then
    # hack to allow --short-circuit on install
    mv bin/java-rmi.cgi sample/rmi
  fi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}

popd

if ! echo $suffix | grep -q "debug" ; then
  # Install Javadoc documentation
  install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir -- $suffix}
cp -a $docdir/jdk*.zip \
     $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir -- $suffix}.zip
  pushd $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir -- $suffix}
    unzip $docdir/jdk*.zip
  popd
fi

# Install desktop files
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole$suffix policytool$suffix ; do
    desktop-file-install --vendor=%{uniquesuffix -- $suffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# FIXME: remove SONAME entries from demo DSOs. See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files"$suffix"
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files"$suffix"
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/sample \
  -type d | sort \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%dir |' \
  >> %{name}-demo.files"$suffix"

# intentionally after all else, fx links  with redirections on its own
%if %{with_openjfx_binding}
  FXSDK_FILES=%{name}-openjfx-devel.files"$suffix"
  FXJRE_FILES=%{name}-openjfx.files"$suffix"
  echo -n "" > $FXJRE_FILES
  echo -n "" > $FXSDK_FILES
  for file in  %{jfx_jre_libs} ; do
    srcfile=%{jfx_jre_libs_dir}/$file
    targetfile=%{_jvmdir}/%{jredir -- $suffix}/lib/$file
    ln -s $srcfile $RPM_BUILD_ROOT/$targetfile
    echo $targetfile >> $FXJRE_FILES
  done
  for file in  %{jfx_jre_native} ; do
    srcfile=%{jfx_jre_native_dir}/$file
    targetfile=%{_jvmdir}/%{jredir -- $suffix}/lib/%{archinstall}/$file
    ln -s $srcfile $RPM_BUILD_ROOT/$targetfile
    echo $targetfile >> $FXJRE_FILES
  done
  for file in  %{jfx_jre_exts} ; do
    srcfile=%{jfx_jre_exts_dir}/$file
    targetfile=%{_jvmdir}/%{jredir -- $suffix}/lib/ext/$file
    ln -s $srcfile $RPM_BUILD_ROOT/$targetfile
    echo $targetfile >> $FXJRE_FILES
  done
  for file in  %{jfx_sdk_libs} ; do
    srcfile=%{jfx_sdk_libs_dir}/$file
    targetfile=%{_jvmdir}/%{sdkdir -- $suffix}/lib/$file
    ln -s $srcfile $RPM_BUILD_ROOT/$targetfile
    echo $targetfile >> $FXSDK_FILES
  done
  for file in  %{jfx_sdk_bins} ; do
    srcfile=%{jfx_sdk_bins_dir}/$file
    targetfile=%{_jvmdir}/%{sdkdir -- $suffix}/bin/$file
    ln -s $srcfile $RPM_BUILD_ROOT/$targetfile
    echo $targetfile >> $FXSDK_FILES
  done
%endif

bash %{SOURCE20} $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir -- $suffix} %{javaver}
# https://bugzilla.redhat.com/show_bug.cgi?id=1183793
touch -t 201401010000 $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir -- $suffix}/lib/security/java.security

# moving config files to /etc
mkdir -p $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}/lib/security/policy/unlimited/
mkdir -p $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}/lib/security/policy/limited/
for file in lib/security/cacerts lib/security/policy/unlimited/US_export_policy.jar lib/security/policy/unlimited/local_policy.jar lib/security/policy/limited/US_export_policy.jar lib/security/policy/limited/local_policy.jar lib/security/java.policy lib/security/java.security lib/security/blacklisted.certs lib/logging.properties lib/calendars.properties lib/security/nss.cfg lib/security/nss.fips.cfg lib/net.properties ; do
  mv      $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir -- $suffix}/$file   $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}/$file
  ln -srv  $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}/$file          $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir -- $suffix}/$file
done

#TODO this is done also i portables and in install jdk. But hard to say where the operation will hapen at the end
# stabilize permissions
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/ -name "*.so" -exec chmod 755 {} \; ;
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/ -type d -exec chmod 755 {} \; ;
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/ -name "ASSEMBLY_EXCEPTION" -exec chmod 644 {} \; ;
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/ -name "LICENSE" -exec chmod 644 {} \; ;
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/ -name "THIRD_PARTY_README" -exec chmod 644 {} \; ;

# end, dual install
done

%check

# We test debug first as it will give better diagnostics on a crash
for suffix in %{build_loop} ; do

# Tests in the check stage are performed on the installed image
# rpmbuild operates as follows: build -> install -> test
export JAVA_HOME=$RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java TestCryptoLevel

# Check ECC is working
$JAVA_HOME/bin/javac -d . %{SOURCE14}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE14})|sed "s|\.java||")

# Check system crypto (policy) is active and can be disabled
# Test takes a single argument - true or false - to state whether system
# security properties are enabled or not.
$JAVA_HOME/bin/javac -d . %{SOURCE15}
export PROG=$(echo $(basename %{SOURCE15})|sed "s|\.java||")
export SEC_DEBUG="-Djava.security.debug=properties"
$JAVA_HOME/bin/java ${SEC_DEBUG} ${PROG} true
$JAVA_HOME/bin/java ${SEC_DEBUG} -Djava.security.disableSystemPropertiesFile=true ${PROG} false

# Check java launcher has no SSB mitigation
if ! nm $JAVA_HOME/bin/java | grep set_speculation ; then true ; else false; fi

# Check alt-java launcher has SSB mitigation on supported architectures
%ifarch %{ssbd_arches}
nm $JAVA_HOME/bin/%{alt_java_name} | grep set_speculation
%else
if ! nm $JAVA_HOME/bin/%{alt_java_name} | grep set_speculation ; then true ; else false; fi
%endif

# Check correct vendor values have been set
$JAVA_HOME/bin/javac -d . %{SOURCE16}
#TODO skipped vendor check. It now points to PORTABLE version of jdk.
#$JAVA_HOME/bin/java $(echo $(basename %{SOURCE16})|sed "s|\.java||") "%{oj_vendor}" "%{oj_vendor_url}" "%{oj_vendor_bug_url}"

# Check translations are available for new timezones
$JAVA_HOME/bin/javac -d . %{SOURCE18}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE18})|sed "s|\.java||") JRE

# Check src.zip has all sources. See RHBZ#1130490
unzip -l $JAVA_HOME/src.zip | grep 'sun.misc.Unsafe'

# debug-symbols are only in debug build
if [ "x$suffix" == "x" ] ; then
  invert="-v"
else
  invert=""
fi

# Check class files include useful debugging information
$JAVA_HOME/bin/javap -l java.lang.Object | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.lang.Object | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.lang.Object | grep $invert LocalVariableTable

# Check generated class files include useful debugging information
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep $invert LocalVariableTable

# build cycles check
done

%if %{include_normal_build}
# intentionally only for non-debug
%pretrans headless -p <lua>
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1290388 for pretrans over pre
-- if copy-jdk-configs is in transaction, it installs in pretrans to temp
-- if copy_jdk_configs is in temp, then it means that copy-jdk-configs is in transaction  and so is
-- preferred over one in %%{_libexecdir}. If it is not in transaction, then depends
-- whether copy-jdk-configs is installed or not. If so, then configs are copied
-- (copy_jdk_configs from %%{_libexecdir} used) or not copied at all
local posix = require "posix"

if (os.getenv("debug") == "true") then
  debug = true;
  print("cjc: in spec debug is on")
else
  debug = false;
end

SOURCE1 = "%{rpm_state_dir}/copy_jdk_configs.lua"
SOURCE2 = "%{_libexecdir}/copy_jdk_configs.lua"

local stat1 = posix.stat(SOURCE1, "type");
local stat2 = posix.stat(SOURCE2, "type");

  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE1 .." exists - copy-jdk-configs in transaction, using this one.")
  end;
  package.path = package.path .. ";" .. SOURCE1
else
  if (stat2 ~= nil) then
  if (debug) then
    print(SOURCE2 .." exists - copy-jdk-configs already installed and NOT in transaction. Using.")
  end;
  package.path = package.path .. ";" .. SOURCE2
  else
    if (debug) then
      print(SOURCE1 .." does NOT exists")
      print(SOURCE2 .." does NOT exists")
      print("No config files will be copied")
    end
  return
  end
end
arg = nil ;  -- it is better to null the arg up, no meter if they exists or not, and use cjc as module in unified way, instead of relaying on "main" method during require "copy_jdk_configs.lua"
cjc = require "copy_jdk_configs.lua"
args = {"--currentjvm", "%{uniquesuffix %{nil}}", "--jvmdir", "%{_jvmdir %{nil}}", "--origname", "%{name}", "--origjavaver", "%{javaver}", "--arch", "%{_arch}", "--temp", "%{rpm_state_dir}/%{name}.%{_arch}"}
cjc.mainProgram(args)

%post
%{post_script %{nil}}

%post headless
%{post_headless %{nil}}

%postun
%{postun_script %{nil}}

%postun headless
%{postun_headless %{nil}}

%posttrans
%{posttrans_script %{nil}}

%posttrans headless
%{alternatives_java_install %{nil}}

%post devel
%{post_devel %{nil}}

%postun devel
%{postun_devel %{nil}}

%posttrans  devel
%{posttrans_devel %{nil}}

%posttrans javadoc
%{alternatives_javadoc_install %{nil}}

%postun javadoc
%{postun_javadoc %{nil}}

%posttrans javadoc-zip
%{alternatives_javadoczip_install %{nil}}

%postun javadoc-zip
%{postun_javadoc_zip %{nil}}
%endif

%if %{include_debug_build}
%post slowdebug
%{post_script -- %{debug_suffix_unquoted}}

%post headless-slowdebug
%{post_headless -- %{debug_suffix_unquoted}}

%posttrans headless-slowdebug
%{alternatives_java_install -- %{debug_suffix_unquoted}}

%postun slowdebug
%{postun_script -- %{debug_suffix_unquoted}}

%postun headless-slowdebug
%{postun_headless -- %{debug_suffix_unquoted}}

%posttrans slowdebug
%{posttrans_script -- %{debug_suffix_unquoted}}

%post devel-slowdebug
%{post_devel -- %{debug_suffix_unquoted}}

%postun devel-slowdebug
%{postun_devel -- %{debug_suffix_unquoted}}

%posttrans  devel-slowdebug
%{posttrans_devel -- %{debug_suffix_unquoted}}
%endif

%if %{include_fastdebug_build}
%post fastdebug
%{post_script -- %{fastdebug_suffix_unquoted}}

%post headless-fastdebug
%{post_headless -- %{fastdebug_suffix_unquoted}}

%postun fastdebug
%{postun_script -- %{fastdebug_suffix_unquoted}}

%postun headless-fastdebug
%{postun_headless -- %{fastdebug_suffix_unquoted}}

%posttrans fastdebug
%{posttrans_script -- %{fastdebug_suffix_unquoted}}

%posttrans headless-fastdebug
%{alternatives_java_install -- %{fastdebug_suffix_unquoted}}

%post devel-fastdebug
%{post_devel -- %{fastdebug_suffix_unquoted}}

%postun devel-fastdebug
%{postun_devel -- %{fastdebug_suffix_unquoted}}

%posttrans  devel-fastdebug
%{posttrans_devel -- %{fastdebug_suffix_unquoted}}

%endif

%if %{include_normal_build}
%files
# main package builds always
%{files_jre %{nil}}
%else
%files
# placeholder
%endif

%if %{include_normal_build}
%files headless
# important note, see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
# all config/noreplace files (and more) have to be declared in pretrans. See pretrans
%{files_jre_headless %{nil}}

%files devel
%{files_devel %{nil}}

%files demo -f %{name}-demo.files
%{files_demo %{nil}}

%files src
%{files_src %{nil}}

%files javadoc
%{files_javadoc %{nil}}

# This puts a huge documentation file in /usr/share
# same for debug variant
%files javadoc-zip
%{files_javadoc_zip %{nil}}

%if %{with_openjfx_binding}
%files openjfx -f %{name}-openjfx.files

%files openjfx-devel -f %{name}-openjfx-devel.files
%endif
%endif

%if %{include_debug_build}
%files slowdebug
%{files_jre -- %{debug_suffix_unquoted}}

%files headless-slowdebug
%{files_jre_headless -- %{debug_suffix_unquoted}}

%files devel-slowdebug
%{files_devel -- %{debug_suffix_unquoted}}

%files demo-slowdebug -f %{name}-demo.files-slowdebug
%{files_demo -- %{debug_suffix_unquoted}}

%files src-slowdebug
%{files_src -- %{debug_suffix_unquoted}}

%if %{with_openjfx_binding}
%files openjfx-slowdebug -f %{name}-openjfx.files-slowdebug

%files openjfx-devel-slowdebug -f %{name}-openjfx-devel.files-slowdebug
%endif
%endif

%if %{include_fastdebug_build}
%files fastdebug
%{files_jre -- %{fastdebug_suffix_unquoted}}

%files headless-fastdebug
%{files_jre_headless -- %{fastdebug_suffix_unquoted}}

%files devel-fastdebug
%{files_devel -- %{fastdebug_suffix_unquoted}}

%files demo-fastdebug  -f %{name}-demo.files-fastdebug
%{files_demo -- %{fastdebug_suffix_unquoted}}

%files src-fastdebug
%{files_src -- %{fastdebug_suffix_unquoted}}

%if %{with_openjfx_binding}
%files openjfx-fastdebug -f %{name}-openjfx.files-fastdebug

%files openjfx-devel-fastdebug -f %{name}-openjfx-devel.files-fastdebug
%endif
%endif

%changelog
%autochangelog
