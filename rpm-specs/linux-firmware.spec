%global debug_package %{nil}

%global _firmwarepath	/usr/lib/firmware
%define _binaries_in_noarch_packages_terminate_build 0

Name:		linux-firmware
Version:	20241017
Release:	2%{?dist}
Summary:	Firmware files used by the Linux kernel
# Automatically converted from old format: GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted - review is highly recommended.
License:	GPL-1.0-or-later AND GPL-2.0-or-later AND LicenseRef-Callaway-MIT AND LicenseRef-Callaway-Redistributable-no-modification-permitted
URL:		http://www.kernel.org/
BuildArch:	noarch

Source0:	https://www.kernel.org/pub/linux/kernel/firmware/%{name}-%{version}.tar.xz

BuildRequires:	make
BuildRequires:	git-core
BuildRequires:	python3
%if %{undefined rhel}
# Not required but de-dupes FW so reduces size
BuildRequires:	rdfind
%endif

Requires:	linux-firmware-whence
Provides:	kernel-firmware = %{version}
Obsoletes:	kernel-firmware < %{version}
Conflicts:	microcode_ctl < 2.1-0

Recommends:	amd-gpu-firmware
Recommends:	intel-gpu-firmware
Recommends:	nvidia-gpu-firmware
%if 0%{?fedora} && 0%{?fedora} < 40
Requires:	amd-ucode-firmware
Requires:	cirrus-audio-firmware
Requires:	intel-audio-firmware
Requires:	nxpwireless-firmware
Requires:	tiwilink-firmware
%else
Recommends:	amd-ucode-firmware
Recommends:	cirrus-audio-firmware
Recommends:	intel-audio-firmware
Recommends:	nxpwireless-firmware
Recommends:	tiwilink-firmware
%endif
Recommends:	atheros-firmware
Recommends:	brcmfmac-firmware
Recommends:	mt7xxx-firmware
Recommends:	realtek-firmware

%description
This package includes firmware files required for some devices to
operate.

%package whence
Summary:	WHENCE License file
# Automatically converted from old format: GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted - review is highly recommended.
License:	GPL-1.0-or-later AND GPL-2.0-or-later AND LicenseRef-Callaway-MIT AND LicenseRef-Callaway-Redistributable-no-modification-permitted
%description whence
This package contains the WHENCE license file which documents the vendor license details.

# GPU firmwares
%package -n amd-gpu-firmware
Summary:	Firmware for AMD GPUs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n amd-gpu-firmware
Firmware for AMD amdgpu and radeon GPUs.

%package -n intel-gpu-firmware
Summary:	Firmware for Intel GPUs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n intel-gpu-firmware
Firmware for Intel GPUs including GuC (Graphics Microcontroller), HuC (HEVC/H.265
Microcontroller) and DMC (Display Microcontroller) firmware for Skylake and later
platforms.

%package -n nvidia-gpu-firmware
Summary:	Firmware for NVIDIA GPUs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n nvidia-gpu-firmware
Firmware for NVIDIA GPUs.

# Microcode updates
%package -n amd-ucode-firmware
Summary:	Microcode updates for AMD CPUs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n amd-ucode-firmware
Microcode updates for AMD CPUs, AMD SEV and AMD TEE.

# WiFi/Bluetooth firmwares
%package -n atheros-firmware
Summary:	Firmware for Qualcomm Atheros WiFi/Bluetooth adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n atheros-firmware
Firmware for Qualcomm Atheros ath6k/ath9k/ath10k/ath11k WiFi adapters.

%package -n brcmfmac-firmware
Summary:	Firmware for Broadcom/Cypress brcmfmac WiFi/Bluetooth adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n brcmfmac-firmware
Firmware for Broadcom/Cypress brcmfmac WiFi/Bluetooth adapters.

%package -n iwlegacy-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 3945(A)BG and 4965AGN adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
Obsoletes:	iwl3945-firmware < %{version}-%{release}
Obsoletes:	iwl4965-firmware < %{version}-%{release}
Provides:	iwl3945-firmware = %{version}-%{release}
Provides:	iwl4965-firmware = %{version}-%{release}
%description -n iwlegacy-firmware
This package contains the firmware required by the iwlegacy driver
for Linux. This includes the 3945(A)BG and 4965AGN WiFi NICs. Usage
of the firmware is subject to the terms and conditions contained
inside the provided LICENSE file. Please read it carefully.

%package -n iwlwifi-dvm-firmware
Summary:	DVM Firmware for Intel(R) Wireless WiFi adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
Obsoletes:	iwl100-firmware < %{version}-%{release}
Obsoletes:	iwl105-firmware < %{version}-%{release}
Obsoletes:	iwl135-firmware < %{version}-%{release}
Obsoletes:	iwl1000-firmware < 1:%{version}-%{release}
Obsoletes:	iwl2000-firmware < %{version}-%{release}
Obsoletes:	iwl2030-firmware < %{version}-%{release}
Obsoletes:	iwl5000-firmware < %{version}-%{release}
Obsoletes:	iwl5150-firmware < %{version}-%{release}
Obsoletes:	iwl6000-firmware < %{version}-%{release}
Obsoletes:	iwl6000g2a-firmware < %{version}-%{release}
Obsoletes:	iwl6000g2b-firmware < %{version}-%{release}
Obsoletes:	iwl6050-firmware < %{version}-%{release}
Provides:	iwl100-firmware = %{version}-%{release}
Provides:	iwl105-firmware = %{version}-%{release}
Provides:	iwl135-firmware = %{version}-%{release}
Provides:	iwl1000-firmware = 1:%{version}-%{release}
Provides:	iwl2000-firmware = %{version}-%{release}
Provides:	iwl2030-firmware = %{version}-%{release}
Provides:	iwl5000-firmware = %{version}-%{release}
Provides:	iwl5150-firmware = %{version}-%{release}
Provides:	iwl6000-firmware = %{version}-%{release}
Provides:	iwl6000g2a-firmware = %{version}-%{release}
Provides:	iwl6000g2b-firmware = %{version}-%{release}
Provides:	iwl6050-firmware = %{version}-%{release}
%description -n iwlwifi-dvm-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with DVM firmware support (CONFIG_IWLDVM=y/m). Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n iwlwifi-mvm-firmware
Summary:	MVM Firmware for Intel(R) Wireless WiFi adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
Obsoletes:	iwl3160-firmware < 1:%{version}-%{release}
Obsoletes:	iwl7260-firmware < 1:%{version}-%{release}
Obsoletes:	iwlax2xx-firmware < %{version}-%{release}
Provides:	iwl3160-firmware = 1:%{version}-%{release}
Provides:	iwl7260-firmware = 1:%{version}-%{release}
Provides:	iwlax2xx-firmware = %{version}-%{release}
%description -n iwlwifi-mvm-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with MVM firmware support (CONFIG_IWLMVM=y/m).  Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n libertas-firmware
Summary:	Firmware for Marvell Libertas SD/USB WiFi Network Adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
Obsoletes:      libertas-sd8686-firmware < %{version}-%{release}
Obsoletes:      libertas-sd8787-firmware < %{version}-%{release}
Obsoletes:      libertas-usb8388-firmware < 2:%{version}-%{release}
Obsoletes:      libertas-usb8388-olpc-firmware < %{version}-%{release}
Provides:       libertas-sd8686-firmware < %{version}-%{release}
Provides:       libertas-sd8787-firmware < %{version}-%{release}
Provides:       libertas-usb8388-firmware < 2:%{version}-%{release}
Provides:       libertas-usb8388-olpc-firmware < %{version}-%{release}
%description -n libertas-firmware
Firmware for the Marvell Libertas series of WiFi Network Adapters
Including the SD 8686/8787 and USB 8388/8388.

%package -n mt7xxx-firmware
Summary:	Firmware for Mediatek 7600/7900 series WiFi/Bluetooth adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n mt7xxx-firmware
Firmware for Mediatek 7600/7900 series WiFi/Bluetooth adapters

%package -n nxpwireless-firmware
Summary:	Firmware for NXP WiFi/Bluetooth/UWB adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n nxpwireless-firmware
Firmware for NXP WiFi/Bluetooth/UWB adapters.

%package -n realtek-firmware
Summary:	Firmware for Realtek WiFi/Bluetooth adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n realtek-firmware
Firmware for Realtek WiFi/Bluetooth adapters

%package -n tiwilink-firmware
Summary:	Firmware for Texas Instruments WiFi/Bluetooth adapters
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n tiwilink-firmware
Firmware for Texas Instruments WiFi/Bluetooth adapters

# SMART NIC and network switch firmwares
%package -n liquidio-firmware
Summary:	Firmware for Cavium LiquidIO Intelligent Server Adapter
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n liquidio-firmware
Firmware for Cavium LiquidIO Intelligent Server Adapter

%package -n mlxsw_spectrum-firmware
Summary:	Firmware for Mellanox Spectrum 1/2/3 Switches
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n mlxsw_spectrum-firmware
Firmware for Mellanox Spectrumi series 1/2/3 ethernet switches.

%package -n mrvlprestera-firmware
Summary:	Firmware for Marvell Prestera Switchdev/ASIC devices
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n mrvlprestera-firmware
Firmware for Marvell Prestera Switchdev/ASIC devices

%package -n netronome-firmware
Summary:	Firmware for Netronome Smart NICs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n netronome-firmware
Firmware for Netronome Smart NICs

%package -n qed-firmware
Summary:	Firmware for Marvell FastLinQ adapters family
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n qed-firmware
Firmware for Marvell FastLinQ adapters family (QDE), this device
supports RoCE (RDMA over Converged Ethernet), iSCSI, iWARP, FCoE
and ethernet including SRIOV, DCB etc.

# Silicon Vendor specific
%package -n qcom-firmware
Summary:	Firmware for Qualcomm SoCs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
Requires:	atheros-firmware = %{version}-%{release}
%description -n qcom-firmware
Firmware for various compoents in Qualcomm SoCs including Adreno
GPUs, Venus video encode/decode, Audio DSP, Compute DSP, WWAN
modem, Sensor DSPs.

# Vision and ISP hardware
%package -n intel-vsc-firmware
Summary:	Firmware files for Intel Visual Sensing Controller (IVSC)
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n intel-vsc-firmware
Firmware files for Intel Visual Sensing Controller (IVSC) for
Tiger Lake, Alder Lake and Raptor Lake SoCs and the IPU3/6 firmware.

# Sound codec hardware
%package -n cirrus-audio-firmware
Summary:	Firmware for Cirrus audio amplifiers and codecs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n cirrus-audio-firmware
Firmware for Cirrus audio amplifiers and codecs

%package -n intel-audio-firmware
Summary:	Firmware for Intel audio DSP amplifiers and codecs
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n intel-audio-firmware
Firmware for Intel audio DSP amplifiers and codecs

# Random other hardware
%package -n dvb-firmware
Summary:	Firmware for various DVB broadcast receivers
# Automatically converted from old format: Redistributable, no modification permitted - review is highly recommended.
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence
%description -n dvb-firmware
Firmware for various DVB broadcast receivers. These include the
Siano DTV devices, devices based on Conexant chipsets (cx18,
cx23885, cx23840, cx231xx), Xceive xc4000/xc5000, DiBcom dib0700,
Terratec H5 DRX-K, ITEtech IT9135 Ax and Bx, and av7110.

%prep
%autosetup -S git -p1

%build

%install
mkdir -p %{buildroot}/%{_firmwarepath}
mkdir -p %{buildroot}/%{_firmwarepath}/updates

make DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwarepath} install-xz
%if %{undefined rhel}
make DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwarepath} dedup
%endif

#Cleanup files we don't want to ship
pushd %{buildroot}/%{_firmwarepath}
# Remove firmware shipped in separate packages already
# Perhaps these should be built as subpackages of linux-firmware?
rm -rf ess korg sb16 yamaha

# Remove firmware for Creative CA0132 HD as it's in alsa-firmware
rm -f ctefx.bin* ctspeq.bin*

# Remove source files we don't need to install
rm -rf carl9170fw
rm -rf cis/{src,Makefile}
rm -f atusb/ChangeLog
rm -f av7110/{Boot.S,Makefile}
rm -f dsp56k/{bootstrap.asm,concat-bootstrap.pl,Makefile}
rm -f iscis/{*.c,*.h,README,Makefile}
rm -f keyspan_pda/{keyspan_pda.S,xircom_pgs.S,Makefile}
rm -f usbdux/*dux */*.asm

# No need to install old firmware versions where we also provide newer versions
# which are preferred and support the same (or more) hardware
rm -f libertas/sd8686_v8*
rm -f libertas/usb8388_v5.bin*

# Remove superfluous infra files
rm -f check_whence.py configure Makefile README
popd

# Create file list but exclude firmwares that we place in subpackages
FILEDIR=`pwd`
pushd %{buildroot}/%{_firmwarepath}
find . \! -type d > $FILEDIR/linux-firmware.files
find . -type d | sed -e '/^.$/d' > $FILEDIR/linux-firmware.dirs
popd
sed -i -e 's:^./::' linux-firmware.{files,dirs}
sed \
	-i -e '/^a300_p/d' \
	-i -e '/^amdgpu/d' \
	-i -e '/^amd/d' \
	-i -e '/^amdtee/d' \
	-i -e '/^amd-ucode/d' \
	-i -e '/^ar3k/d' \
	-i -e '/^ath6k/d' \
	-i -e '/^ath9k_htc/d' \
	-i -e '/^ath10k/d' \
	-i -e '/^ath11k/d' \
	-i -e '/^ath12k/d' \
	-i -e '/^as102_data/d' \
	-i -e '/^av7110/d' \
	-i -e '/^brcm/d' \
	-i -e '/^cirrus/d' \
	-i -e '/^cmmb/d' \
	-i -e '/^cypress/d' \
	-i -e '/^dvb/d' \
	-i -e '/^i915/d' \
	-i -e '/^intel\/avs/d' \
	-i -e '/^intel\/catpt/d' \
	-i -e '/^intel\/dsp_fw/d' \
	-i -e '/^intel\/fw_sst/d' \
	-i -e '/^intel\/ipu/d' \
	-i -e '/^intel\/ipu3/d' \
	-i -e '/^intel\/irci_irci/d' \
	-i -e '/^intel\/vsc/d' \
	-i -e '/^isdbt/d' \
	-i -e '/^iwlwifi/d' \
	-i -e '/^nvidia\/a/d' \
	-i -e '/^nvidia\/g/d' \
	-i -e '/^nvidia\/tu/d' \
	-i -e '/^lgs8g75/d' \
	-i -e '/^libertas/d' \
	-i -e '/^liquidio/d' \
	-i -e '/^mellanox/d' \
	-i -e '/^mediatek\/mt76/d' \
	-i -e '/^mediatek\/mt79/d' \
	-i -e '/^mediatek\/BT/d' \
	-i -e '/^mediatek\/WIFI/d' \
	-i -e '/^mrvl\/prestera/d' \
	-i -e '/^mrvl\/sd8787/d' \
	-i -e '/^mt76/d' \
	-i -e '/^netronome/d' \
	-i -e '/^nxp/d' \
	-i -e '/^qca/d' \
	-i -e '/^qcom/d' \
	-i -e '/^qed/d' \
	-i -e '/^radeon/d' \
	-i -e '/^rtl_bt/d' \
	-i -e '/^rtlwifi/d' \
	-i -e '/^rtw88/d' \
	-i -e '/^rtw89/d' \
	-i -e '/^sms1xxx/d' \
	-i -e '/^tdmb/d' \
	-i -e '/^ti-connectivity/d' \
	-i -e '/^v4l-cx2/d' \
	linux-firmware.files
sed -i -e 's!^!/usr/lib/firmware/!' linux-firmware.{files,dirs}
sed -i -e 's/^/"/;s/$/"/' linux-firmware.files
sed -e 's/^/%%dir /' linux-firmware.dirs >> linux-firmware.files


%files -f linux-firmware.files
%dir %{_firmwarepath}
%license LICENCE.* LICENSE.* GPL*

%files whence
%license WHENCE

# GPU firmwares
%files -n amd-gpu-firmware
%license LICENSE.radeon LICENSE.amdgpu
%{_firmwarepath}/amdgpu/
%{_firmwarepath}/radeon/

%files -n intel-gpu-firmware
%license LICENSE.i915
%{_firmwarepath}/i915/

%files -n nvidia-gpu-firmware
%license LICENCE.nvidia
%dir %{_firmwarepath}/nvidia/
%{_firmwarepath}/nvidia/a*/
%{_firmwarepath}/nvidia/g*/
%{_firmwarepath}/nvidia/tu*/

# Microcode updates
%files -n amd-ucode-firmware
%license LICENSE.amd-ucode
%{_firmwarepath}/amd/
%{_firmwarepath}/amdtee/
%{_firmwarepath}/amd-ucode/

# WiFi/Bluetooth firmwares
%files -n atheros-firmware
%license LICENCE.atheros_firmware
%license LICENSE.QualcommAtheros_ar3k
%license LICENSE.QualcommAtheros_ath10k
%license LICENCE.open-ath9k-htc-firmware
%license qca/NOTICE.txt
%{_firmwarepath}/ar3k/
%{_firmwarepath}/ath6k/
%{_firmwarepath}/ath9k_htc/
%{_firmwarepath}/ath10k/
%{_firmwarepath}/ath11k/
%{_firmwarepath}/ath12k/
%{_firmwarepath}/qca/

%files -n brcmfmac-firmware
%license LICENCE.broadcom_bcm43xx
%license LICENCE.cypress
%{_firmwarepath}/brcm/
%{_firmwarepath}/cypress/

%files -n iwlegacy-firmware
%license LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-3945-*.ucode*
%{_firmwarepath}/iwlwifi-4965-*.ucode*

%files -n iwlwifi-dvm-firmware
%license LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-100-*.ucode*
%{_firmwarepath}/iwlwifi-105-*.ucode*
%{_firmwarepath}/iwlwifi-135-*.ucode*
%{_firmwarepath}/iwlwifi-1000-*.ucode*
%{_firmwarepath}/iwlwifi-2000-*.ucode*
%{_firmwarepath}/iwlwifi-2030-*.ucode*
%{_firmwarepath}/iwlwifi-5000-*.ucode*
%{_firmwarepath}/iwlwifi-5150-*.ucode*
%{_firmwarepath}/iwlwifi-6000-*.ucode*
%{_firmwarepath}/iwlwifi-6000g2a-*.ucode*
%{_firmwarepath}/iwlwifi-6000g2b-*.ucode*
%{_firmwarepath}/iwlwifi-6050-*.ucode*

%files -n iwlwifi-mvm-firmware
%license LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-3160-*.ucode*
%{_firmwarepath}/iwlwifi-3168-*.ucode*
%{_firmwarepath}/iwlwifi-7260-*.ucode*
%{_firmwarepath}/iwlwifi-7265-*.ucode*
%{_firmwarepath}/iwlwifi-7265D-*.ucode*
%{_firmwarepath}/iwlwifi-8000C-*.ucode*
%{_firmwarepath}/iwlwifi-8265-*.ucode*
%{_firmwarepath}/iwlwifi-9000-*.ucode*
%{_firmwarepath}/iwlwifi-9260-*.ucode*
%{_firmwarepath}/iwlwifi-cc-a0-*.ucode*
%{_firmwarepath}/iwlwifi-gl-c0*
%{_firmwarepath}/iwlwifi-ma-b0*
%{_firmwarepath}/iwlwifi-Qu*.ucode*
%{_firmwarepath}/iwlwifi-ty-a0*
%{_firmwarepath}/iwlwifi-so-a0*
%{_firmwarepath}/iwlwifi-bz-b0*

%files -n libertas-firmware
%license LICENCE.Marvell LICENCE.OLPC
%dir %{_firmwarepath}/libertas
%dir %{_firmwarepath}/mrvl
%{_firmwarepath}/libertas/*
%{_firmwarepath}/mrvl/sd8787*

%files -n mt7xxx-firmware
%license LICENCE.mediatek
%license LICENCE.ralink_a_mediatek_company_firmware
%dir %{_firmwarepath}/mediatek
%{_firmwarepath}/mediatek/mt76*
%{_firmwarepath}/mediatek/mt79*
%{_firmwarepath}/mediatek/BT*
%{_firmwarepath}/mediatek/WIFI*
%{_firmwarepath}/mt76*

%files -n nxpwireless-firmware
%license LICENSE.nxp
%dir %{_firmwarepath}/nxp
%{_firmwarepath}/nxp/*

%files -n realtek-firmware
%license LICENCE.rtlwifi_firmware.txt
%{_firmwarepath}/rtl_bt/
%{_firmwarepath}/rtlwifi/
%{_firmwarepath}/rtw88/
%{_firmwarepath}/rtw89/

%files -n tiwilink-firmware
%license LICENCE.ti-connectivity
%dir %{_firmwarepath}/ti-connectivity/
%{_firmwarepath}/ti-connectivity/*

# SMART NIC and network switch firmwares
%files -n liquidio-firmware
%license LICENCE.cavium_liquidio
%dir %{_firmwarepath}/liquidio
%{_firmwarepath}/liquidio/*

%files -n mrvlprestera-firmware
%license LICENCE.Marvell
%dir %{_firmwarepath}/mrvl/prestera
%{_firmwarepath}/mrvl/prestera/*

%files -n mlxsw_spectrum-firmware
%dir %{_firmwarepath}/mellanox/
%{_firmwarepath}/mellanox/*

%files -n netronome-firmware
%license LICENCE.Netronome
%dir %{_firmwarepath}/netronome
%{_firmwarepath}/netronome/*

%files -n qed-firmware
%dir %{_firmwarepath}/qed
%{_firmwarepath}/qed/*

# Silicon Vendor specific
%files -n qcom-firmware
%license LICENSE.qcom LICENSE.qcom_yamato qcom/NOTICE.txt
%dir %{_firmwarepath}/qcom
%{_firmwarepath}/qcom/*
%{_firmwarepath}/a300_p*

# Vision and ISP hardware
%files -n intel-vsc-firmware
%license LICENSE.ivsc
%dir %{_firmwarepath}/intel/ipu/
%dir %{_firmwarepath}/intel/vsc/
%{_firmwarepath}/intel/ipu3-fw.bin*
%{_firmwarepath}/intel/irci_irci_ecr-master_20161208_0213_20170112_1500.bin*
%{_firmwarepath}/intel/ipu/*
%{_firmwarepath}/intel/vsc/*

# Sound codec hardware
%files -n cirrus-audio-firmware
%license LICENSE.cirrus
%dir %{_firmwarepath}/cirrus
%{_firmwarepath}/cirrus/*

%files -n intel-audio-firmware
%license LICENCE.adsp_sst LICENCE.IntcSST2
%dir %{_firmwarepath}/intel/
%dir %{_firmwarepath}/intel/avs/
%dir %{_firmwarepath}/intel/catpt/
%{_firmwarepath}/intel/avs/*
%{_firmwarepath}/intel/catpt/*
%{_firmwarepath}/intel/dsp_fw*
%{_firmwarepath}/intel/fw_sst*

# Random other hardware
%files -n dvb-firmware
%license LICENSE.dib0700 LICENCE.it913x LICENCE.siano
%license LICENCE.xc4000 LICENCE.xc5000 LICENCE.xc5000c
%dir %{_firmwarepath}/av7110/
%{_firmwarepath}/av7110/*
%{_firmwarepath}/as102_data*
%{_firmwarepath}/cmmb*
%{_firmwarepath}/dvb*
%{_firmwarepath}/isdbt*
%{_firmwarepath}/lgs8g75*
%{_firmwarepath}/sms1xxx*
%{_firmwarepath}/tdmb*
%{_firmwarepath}/v4l-cx2*

%changelog
* Sat Oct 19 2024 Adam Williamson <awilliam@redhat.com> - 20241017-2
- Fix compression / deduplication for upstream changes in 20241017

* Thu Oct 17 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20241017-1
- Update to upstream 20241017
- rtlwifi: Update firmware for RTL8192FU to v7.3
- Remove execute bit from firmware files
- rtl_nic: add firmware rtl8125d-1
- iwlwifi: add gl/Bz FW for core91-69 release
- iwlwifi: update ty/So/Ma firmwares for core91-69 release
- iwlwifi: update cc/Qu/QuZ firmwares for core91-69 release
- cirrus: cs35l56: Add firmware for Cirrus CS35L56 for somt7996me ASUS/HP/Lenovo Laptops
- update firmware for en8811h 2.5G ethernet phy
- mtk_wed: add firmware for mt7988 Wireless Ethernet Dispatcher
- ath12k: WCN7850 hw2.0: update board-2.bin
- ath12k: QCN9274 hw2.0: add to WLAN.WBE.1.3.1-00162-QCAHKSWPL_SILICONZ-1
- ath12k: QCN9274 hw2.0: add board-2.bin
- Add a link from TAS2XXX1EB3.bin -> ti/tas2781/TAS2XXX1EB30.bin
- tas2781: Upload dsp firmware for ASUS laptop 1EB30 & 1EB31
- rtlwifi: Add firmware v39.0 for RTL8192DU
- Revert "ath12k: WCN7850 hw2.0: update board-2.bin"
- QCA: Add Bluetooth firmwares for WCN785x with UART transport
- amdgpu: DMCUB DCN35 update
- brcm: Add BCM4354 NVRAM for Jetson TX1
- brcm: Link FriendlyElec NanoPi M4 to AP6356S nvram
- add firmware for MediaTek Bluetooth chip (MT7920)
- add firmware for MT7920
- amdgpu: update numerous firmware
- qcom: update gpu firmwares for qcm6490 chipset
- mt76: mt7996: add firmware files for mt7992/mt7996 chipset variants
- qcom: add gpu firmwares for sa8775p chipset
- rtw89: 8922a: add fw format-2 v0.35.42.1
- WHENCE: Fix battmgr.jsn entry type
- qcom: qcm6490: add ADSP and CDSP firmware
- Update firmware file for various Intel Bluetooth
- rtl_bt: Update RTL8852B BT USB FW to 0x0447_9301
- realtek: rt1320: Add patch firmware of MCU

* Mon Sep  9 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240909-1
- Update to upstream 20240909
- i915: Update MTL DMC v2.23
- cirrus: cs35l56: Add firmware for Cirrus CS35L54 for some HP laptops
- amdgpu: Revert sienna cichlid dmcub firmware update
- iwlwifi: add Bz FW for core89-58 release
- rtl_nic: add firmware rtl8126a-3
- update  MT7921 WiFi/bluetooth device firmware
- amdgpu: update DMCUB to v0.0.232.0 for DCN314 and DCN351
- amdgpu: DMCUB updates forvarious AMDGPU ASICs
- rtw89: 8922a: add fw format-1 v0.35.41.0
- update  MT7925 WiFi/bluetooth device firmware
- rtl_bt: Add firmware and config files for RTL8922A
- rtl_bt: Add firmware file for the the RTL8723CS Bluetooth part
- rtl_bt: de-dupe identical config.bin files
- rename rtl8723bs_config-OBDA8723.bin -> rtl_bt/rtl8723bs_config.bin
- Update AMD SEV firmware
- update firmware for MT7996
- Revert "i915: Update MTL DMC v2.22"
- ath12k: WCN7850 hw2.0: update board-2.bin
- ath11k: WCN6855 hw2.0: update to WLAN.HSP.1.1-03125-QCAHSPSWPL_V1_V2_SILICONZ_LITE-3.6510.41
- ath11k: WCN6855 hw2.0: update board-2.bin
- ath11k: QCA2066 hw2.1: add to WLAN.HSP.1.1-03926.13-QCAHSPSWPL_V2_SILICONZ_CE-2.52297.3
- ath11k: QCA2066 hw2.1: add board-2.bin
- ath11k: IPQ5018 hw1.0: update to WLAN.HK.2.6.0.1-01291-QCAHKSWPL_SILICONZ-1
- qcom: vpu: add video firmware for sa8775p
- amdgpu: DMCUB updates for various AMDGPU ASICs

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 20240811-3
- convert license to SPDX

* Fri Aug 16 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240811-2
- Delete intel sound topology files - duped in alsa-sof-firmware

* Mon Aug 12 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240811-1
- Update to upstream 20240811
- qcom: update path for video firmware for vpu-1/2/3.0
- QCA: Update Bluetooth WCN685x 2.1 firmware to 2.1.0-00642
- rtw89: 8852c: add fw format-1 v0.27.97.0
- rtw89: 8852bt: add firmware 0.29.91.0
- amdgpu: A lot of firmware updates
- mediatek: Update mt8195 SOF firmware
- xe: First GuC release v70.29.2 for BMG
- xe: Add GuC v70.29.2 for LNL
- i915: Add GuC v70.29.2 for ADL-P, DG1, DG2, MTL, and TGL
- i915: Update MTL DMC v2.22, MTL GSC to v102.0.10.1878
- xe: Add BMG HuC 8.2.10, GSC 104.0.0.1161 for LNL, LNL HuC 9.4.13
- i915: update DG2 HuC to v7.10.16
- QCA: Update Bluetooth QCA2066 firmware to 2.1.0-00641
- update firmware for MT7921/MT7922 WiFi device
- update firmware for mediatek bluetooth chip (MT7921/MT7922)
- iwlwifi: add gl FW for core89-58 release
- iwlwifi: update cc/Qu/QuZ firmwares for core89-58 release
- mediatek: Update mt8195 SOF firmware and sof-tplg
- ASoC: tas2781: fix the license issue for tas781 firmware
- rtl_bt: Update RTL8852B BT USB FW to 0x048F_4008
- i915: Update Xe2LPD DMC to v2.21
- qcom: move signed x1e80100 signed firmware to the SoC subdir
- qcom: add video firmware file for vpu-3.0
- amdgpu: update DMCUB to v0.0.225.0 for Various AMDGPU Asics
- qcom: add gpu firmwares for x1e80100 chipset
- add firmware for qat_402xx devices
- Update AMD cpu microcode
- intel: avs: Add numerous sound topology files
- Add a copy of Apache-2.0
- intel: avs: Update AudioDSP base firmware for APL-based platforms

* Wed Jul 10 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240709-1
- Update to upstream 20240709
- Add ISH firmware file for Intel Lunar Lake platform
- amdgpu: update DMCUB to v0.0.224.0 for Various AMDGPU Asics
- cirrus: cs35l41: Update various firmware for ASUS laptops using CS35L41
- amdgpu: Update ISP FW for isp v4.1.1
- mediatek: Update MT8173 VPU firmware to v1.2.0
- qcom: Add AIC100 firmware files
- amlogic: Update bluetooth firmware binary
- Various Intel Bluetooth firmware updates
- rtl_bt: Update RTL8822C BT UART/USB firmware
- amdgpu: update DMCUB to v0.0.222.0 for DCN314
- iwlwifi: add ty/So/Ma firmwares for core88-87 release
- iwlwifi: update cc/Qu/QuZ firmwares for core88-87 release
- add new cc33xx firmware for TI cc33xx WiFi chips
- cirrus: cs35l56: Update firmware for Cirrus CS35L56 for various ASUS laptops

* Tue Jun 11 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240610-1
- Update to upstream 20240610
- Add firmware for Lenovo Thinkbooks
- amdgpu: numerous firmware additions/updates
- QCA: Update Bluetooth QCA2066 firmware to 2.1.0-00639
- cnm: update chips&media wave521c firmware.
- Add ordinary firmware for RTL8821AU device

* Mon May 13 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240513-1
- Update to upstream 20240513
- Splitout Marvell FastLinQ adapter firmware to sub-package
- amdgpu: DMCUB updates for various AMDGPU ASICs
- Amphion: Update vpu firmware
- Update firmware Intel Bluetooth BlazarU/Solar/Magnetor
- i915: Add BMG DMC v2.06
- Add CS35L41 HDA Firmware for Asus HN7306
- Tuning for HP Consumer Laptop
- amdgpu: DMCUB updates for various AMDGPU ASICs
- rtl_bt: Update RTL8822C BT UART firmware to 0x0FD6_407B
- rtl_bt: Update RTL8822C BT USB firmware to 0x0ED6_407B
- cirrus: cs35l56: Add firmware for Cirrus CS35L56 for various ASUS laptops
- Add firmware and tuning for Lenovo Y770S
- amdgpu: DMCUB updates for various AMDGPU ASICs
- Add firmware for Cirrus CS35L56 for various HP laptops
- i915: Update Xe2LPD DMC to v2.20
- Remove Calibration Firmware and Tuning for CS35L41
- Add firmware for Lenovo Thinkbook 13X
- ASoC: tas2781: Add dsp firmware for Thinkpad ICE-1 laptop
- amdgpu: Numerous firmware updates
- Montage: update firmware for Mont-TSSE
- Add tuning parameter configs for CS35L41 Firmware
- Fix firmware names for Laptop SSID 104316a3
- Add CS35L41 HDA Firmware for Lenovo Legion Slim 7 16ARHA7
- update mediatek bluetooth chip (MT7922)
- update MT7922 WiFi device FW
- iwlwifi: updates/additions for core87-44 release
- nvidia: Update Tegra210 XUSB firmware to v50.29
- mediatek: Update MT8173 VPU firmware to v1.1.9

* Wed Apr 10 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240410-1
- Update to upstream 20240410
- ath10k: WCN3990: hw1.0: add qcm2290 firmware API file
- ath10k: WCN3990: hw1.0: move firmware back from qcom/ location
- i915: Add DG2 HuC 7.10.15
- amdgpu: DMCUB updates for various AMDGPU ASICs
- update firmware for en8811h 2.5G ethernet phy
- mekdiatek: Update mt8186 SOF firmware to v2.0.1
- rtw89: 8852c: update fw to v0.27.56.14
- rtw89: 8922a: add firmware v0.35.18.0
- rtw88: Add RTL8703B firmware v11.0.0
- Add firmware for Cirrus CS35L56 for Dell laptops
- Montage: update firmware for Mont-TSSE
- WHENCE: Link the Raspberry Pi CM4 and 5B to the 4B
- Update firmware for Intel Bluetooth 9260/9560/AX101/AX200/AX201/AX203/AX210/AX211/BE200
- amdgpu: DMCUB updates for various AMDGPU ASICs
- mediatek: Update MT8173 VPU firmware to v1.1.8
- imx: sdma: update firmware to v3.6/v4.6

* Tue Mar 12 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240312-1
- Update to upstream 20240312
- iwlwifi: update 9000-family firmwares to core85-89
- rtl_bt: Update RTL8852A BT USB firmware to 0xD9D6_17DA
- update firmware for MT7922/MT7921 WiFi device
- update firmware for mediatek bluetooth chip (MT7922)
- update firmware for mediatek bluetooth chip (MT7921)
- Add CS35L41 HDA Firmware for Lenovo Thinkbook 16P Laptops
- amdgpu: Update VCN firmware binaries
- Intel IPU2: Add firmware files
- brcm: Add nvram for the Acer Iconia One 7 B1-750 tablet
- i915: Add Xe2LPD DMC v2.18
- i915: Update MTL DMC v2.21

* Tue Feb 20 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240220-1
- Update to upstream 20240220
- update firmware for en8811h 2.5G ethernet phy
- add firmware for MT7996
- xe: First GuC release for LNL and Xe
- i915: Add GuC v70.20.0 for ADL-P, DG1, DG2, MTL and TGL
- Add CS35L41 firmware for Lenovo Legion 7i gen7 laptop (16IAX7)
- brcm: Add nvram for the Asus Memo Pad 7 ME176C tablet
- ice: update ice DDP package to 1.3.36.0
- Add CS35L41 firmware for additional ASUS Zenbook 2023 models
- panthor: Add initial firmware for Gen10 Arm Mali GPUs
- qcom: update venus firmware file for v5.4
- Montage: add firmware for Mont-TSSE
- Remove 2 HP laptops using CS35L41 Audio Firmware
- Fix filenames for some CS35L41 firmwares for HP
- wilc1000: update WILC1000 firmware to v16.1.2
- rtl_nic: add firmware for RTL8126A
- intel: Add IPU6 firmware binaries
- ath11k: WCN6855 hw2.0: update to WLAN.HSP.1.1-03125-QCAHSPSWPL_V1_V2_SILICONZ_LITE-3.6510.37
- qcom: Add Audio firmware for SM8550 HDK
- brcm: Add brcmfmac43430-sdio.xxx.txt nvram for the Chuwi Hi8 (CWI509) tablet
- qcom: Add Audio firmware for SM8650 MTP
- Add firmware for Cirrus CS35L41 on HP Consumer Laptops
- amdgpu: lots of firmware updates ¯\_(ツ)_/¯
- Update AMD cpu microcode
- RTL8192E: Remove old realtek WiFi firmware

* Thu Jan 18 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 20240115-2
- Update some firmware filters

* Mon Jan 15 2024 Peter Robinson <pbrobinson@fedoraproject.org>
- Update to upstream 20240115
- Split out Intel/Cirrus audio firmware, ISP firmware, NXP/TI WiFi Firmware
- Intel Bluetooth: Update firmware file for AX101/AX203/AX210/AX211
- Cirrus: Add CS35L41 firmware for Legion Slim 7 Gen 8 laptops
- Cirrus: Add firmware for CS35L41 for various Dell laptops
- update firmware for qat_4xxx devices
- update firmware for w1u_uart
- Cirrus: Add firmware file for cs42l43
- amdgpu: DMCUB updates for DCN312/DCN314
- amlogic/bluetooth: add firmware bin of W1 serial soc(w1u_uart)
- Add firmware for Mediatek WiFi/bluetooth chip (MT7925)
- ASoC: tas2781/tas2563: Add dsp firmware for laptops or other mobile devices
- rtl_bt: Add firmware and config files for RTL8852BT/RTL8852BE-VT
- ath11k: Updates for WCN6855/WCN6750/IPQ8074
- ath10k: Updates to WCN3990/QCA9888/QCA4019/QCA6174
- ath12k: add new driver and firmware for WCN7850
- iwlwifi: update gl FW for core80-165 release
- intel: vsc: Add firmware for Visual Sensing Controller
- Cirrus: Add CS35L41 firmware and tunings for ASUS Zenbook 2022/2023 Models
- QCA: Add bluetooth firmware nvm files for QCA2066
- QCA: Update Bluetooth QCA2066 firmware to 2.1.0-00629
- amdgpu: DMCUB updates for various AMDGPU ASICs
- qcom: Add Audio firmware for SM8550/SM8650 QRD