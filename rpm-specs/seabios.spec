%if 0%{?fedora:1}
%define cross 1
%endif

Name:           seabios
Version:        1.16.3
Release:        %autorelease
Summary:        Open-source legacy BIOS implementation

License:        LGPL-3.0-only
URL:            http://www.coreboot.org/SeaBIOS

Source0:        http://code.coreboot.org/p/seabios/downloads/get/%{name}-%{version}.tar.gz

Patch0001:      0001-Workaround-for-a-win8.1-32-S4-resume-bug.patch
Patch0003:      0003-vgabios-Reorder-video-modes-to-work-around-a-Windows.patch

Source10:       config.vga-cirrus
Source11:       config.vga-isavga
Source12:       config.vga-qxl
Source13:       config.vga-stdvga
Source14:       config.vga-vmware
Source15:       config.csm
Source16:       config.coreboot
Source17:       config.seabios-128k
Source18:       config.seabios-256k
Source19:       config.vga-virtio
Source20:       config.vga-ramfb
Source21:       config.vga-bochs-display
Source22:       config.vga-ati
Source23:       config.seabios-microvm

BuildRequires: make
BuildRequires: gcc
BuildRequires: python3
%if 0%{?cross:1}
BuildRequires: binutils-x86_64-linux-gnu gcc-x86_64-linux-gnu
Buildarch:     noarch
%else
ExclusiveArch: x86_64
%endif

Requires: %{name}-bin = %{version}-%{release}
Requires: seavgabios-bin = %{version}-%{release}

# Seabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

# Similarly, tell RPM to not complain about x86 roms being shipped noarch
%global _binaries_in_noarch_packages_terminate_build   0

# You can build a debugging version of the BIOS by setting this to a
# value > 1.  See src/config.h for possible values, but setting it to
# a number like 99 will enable all possible debugging.  Note that
# debugging goes to a special qemu port that you have to enable.  See
# the SeaBIOS top-level README file for the magic qemu invocation to
# enable this.
%global debug_level 1


%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package bin
Summary: Seabios for x86
Buildarch: noarch


%description bin
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package -n seavgabios-bin
Summary: Seavgabios for x86
Buildarch: noarch

%description -n seavgabios-bin
SeaVGABIOS is an open-source VGABIOS implementation.


%prep
%setup -q
%autopatch -p1

%build
%define _lto_cflags %{nil}
export CFLAGS="$RPM_OPT_FLAGS"
mkdir binaries

build_bios() {
    make clean distclean
    cp $1 .config
    echo "CONFIG_DEBUG_LEVEL=%{debug_level}" >> .config
    make oldnoconfig V=1

    make V=1 \
        EXTRAVERSION="-%{release}" \
        PYTHON=python3 \
%if 0%{?cross:1}
        HOSTCC=gcc \
        CC=x86_64-linux-gnu-gcc \
        AS=x86_64-linux-gnu-as \
        LD=x86_64-linux-gnu-ld \
        OBJCOPY=x86_64-linux-gnu-objcopy \
        OBJDUMP=x86_64-linux-gnu-objdump \
        STRIP=x86_64-linux-gnu-strip \
%endif
        $4

    cp out/$2 binaries/$3
}

# seabios
build_bios %{_sourcedir}/config.seabios-128k bios.bin bios.bin
build_bios %{_sourcedir}/config.seabios-256k bios.bin bios-256k.bin
%if 0%{?fedora:1}
build_bios %{_sourcedir}/config.csm Csm16.bin bios-csm.bin
build_bios %{_sourcedir}/config.coreboot bios.bin.elf bios-coreboot.bin
build_bios %{_sourcedir}/config.seabios-microvm bios.bin bios-microvm.bin
%endif

# seavgabios
%global vgaconfigs bochs-display cirrus isavga qxl stdvga ramfb vmware virtio ati
for config in %{vgaconfigs}; do
    build_bios %{_sourcedir}/config.vga-${config} \
               vgabios.bin vgabios-${config}.bin out/vgabios.bin
done


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seabios
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seavgabios
install -m 0644 binaries/bios.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios.bin
install -m 0644 binaries/bios-256k.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-256k.bin
%if 0%{?fedora:1}
install -m 0644 binaries/bios-csm.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-csm.bin
install -m 0644 binaries/bios-coreboot.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-coreboot.bin
install -m 0644 binaries/bios-microvm.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-microvm.bin
%endif
install -m 0644 binaries/vgabios*.bin $RPM_BUILD_ROOT%{_datadir}/seavgabios


%files
%doc COPYING COPYING.LESSER README


%files bin
%dir %{_datadir}/seabios/
%{_datadir}/seabios/bios*.bin

%files -n seavgabios-bin
%dir %{_datadir}/seavgabios/
%{_datadir}/seavgabios/vgabios*.bin


%changelog
%autochangelog
