# Disable the growpart subpackage in EPEL, as RHEL ships it on its own
%if 0%{?epel}
%bcond_with growpart
%else
%bcond_without growpart
%endif

Summary:	Cloud image management utilities
Name:		cloud-utils
Version:	0.33
Release:	%autorelease
License:	GPL-3.0-only
URL:		https://github.com/canonical/%{name}

Source:		%{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:	noarch

Requires:	%{name}-growpart
Requires:	%{name}-cloud-localds
Requires:	%{name}-write-mime-multipart
Requires:	%{name}-ec2metadata
Requires:	%{name}-resize-part-image
Requires:	%{name}-mount-image-callback
Requires:	%{name}-vcs-run

%description
This package provides a useful set of utilities for managing cloud images.

The tasks associated with image bundling are often tedious and repetitive. The
cloud-utils package provides several scripts that wrap the complicated tasks
with a much simpler interface.


%if %{with growpart}
%package growpart
Summary:	A script for growing a partition

Requires:	gawk
Requires:	util-linux
Recommends:	lvm2


%description growpart
This package provides the growpart script for growing a partition. It is
primarily used in cloud images in conjunction with the dracut-modules-growroot
package to grow the root partition on first boot.
%endif


%package cloud-localds
Summary:	A script for creating a nocloud configuration disk for cloud-init

Recommends:	tar
Recommends:	dosfstools
Recommends:	mtools
Recommends:	genisoimage
Recommends:	qemu-img


%description cloud-localds
This package provides the cloud-localds script, which creates a disk-image
with user-data and/or meta-data for cloud-init.


%package write-mime-multipart
Summary:	A utilty for creating mime-multipart files


%description write-mime-multipart
This package provides the write-mime-multipart script, which creates
mime multipart files that can be consumed by cloud-init as user-data.


%package ec2metadata
Summary:	A script to query and display EC2 AMI instance metadata


%description ec2metadata
This package provides the ec2metadata script, which can be used to query and
display EC2 instance metadata rekated to an AMI instance.


%package resize-part-image
Summary:	A script for resizing cloud images

Requires:	file
Requires:	gzip
Requires:	e2fsprogs
Requires:	gawk
Requires:	tar


%description resize-part-image
This package provides the resize-part-image script, which can be used to
resize a partition image and the contained filesystem to a new size.


%package mount-image-callback
Summary:	A script to run commands over cloud image contents

Requires:	gawk
Requires:	util-linux
Recommends:	qemu-img


%description mount-image-callback
This package provides the mount-image-callback script, which mounts a cloud
image to a temporary mountpoint and runs a specified command on the contents.


%package vcs-run
Summary:	Script to run commands over a VCS repository contents

Recommends:	breezy
Recommends:	git-core
Recommends:	mercurial
Recommends:	wget


%description vcs-run
This package provides the vcs-run script, which fetches a code repository
into a temporary directory and runs a user-specified command in it.


%prep
%setup -q

%build

%install

# Create the target directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1

# Install binaries and manpages
install -pm 0755 bin/* %{buildroot}%{_bindir}/
install -pm 0644 man/* %{buildroot}%{_mandir}/man1/

# Exclude Ubuntu-specific tools
rm %{buildroot}%{_bindir}/*ubuntu*

# Exclude the cloud-run-instances manpage
rm -f %{buildroot}%{_mandir}/man1/cloud-run-instances.*

# Exclude euca2ools wrappers and manpages
rm -f %{buildroot}%{_bindir}/cloud-publish-*
rm -f %{buildroot}%{_mandir}/man1/cloud-publish-*

%if %{without growpart}
rm -f %{buildroot}%{_bindir}/growpart
rm -f %{buildroot}%{_mandir}/man1/growpart.*
%endif


%files
%doc ChangeLog
%license LICENSE


%if %{with growpart}
%files growpart
%doc ChangeLog
%license LICENSE
%{_bindir}/growpart
%doc %{_mandir}/man1/growpart.*
%endif


%files cloud-localds
%doc ChangeLog
%license LICENSE
%{_bindir}/cloud-localds
%doc %{_mandir}/man1/cloud-localds.*


%files write-mime-multipart
%doc ChangeLog
%license LICENSE
%{_bindir}/write-mime-multipart
%doc %{_mandir}/man1/write-mime-multipart.*


%files ec2metadata
%doc ChangeLog
%license LICENSE
%{_bindir}/ec2metadata


%files resize-part-image
%doc ChangeLog
%license LICENSE
%{_bindir}/resize-part-image
%doc %{_mandir}/man1/resize-part-image.*


%files mount-image-callback
%doc ChangeLog
%license LICENSE
%{_bindir}/mount-image-callback


%files vcs-run
%doc ChangeLog
%license LICENSE
%{_bindir}/vcs-run


%changelog
%autochangelog
