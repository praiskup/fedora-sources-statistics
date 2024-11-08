Name:           ntfs2btrfs
Version:        20240115
Release:        %autorelease
Summary:        Conversion tool from NTFS to Btrfs

License:        GPL-2.0-or-later
URL:            https://github.com/maharmstone/ntfs2btrfs
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         https://github.com/maharmstone/ntfs2btrfs/commit/4375a142fe635044fe54e0c897bdc2bd07225d97.patch#/%{name}-gcc-14.1-include-memory.diff

BuildRequires:  cmake >= 3.14.3
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake(fmt)
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(lzo2)
BuildRequires:  pkgconfig(libzstd)

# Adapted for specific use in this program, cannot be reasonably separated
Provides:       bundled(ntfs-3g-system-compression)

# Upstream doesn't have big endian support in the handwritten assembler
ExcludeArch:    ppc64 s390x

%description
ntfs2btrfs is a tool which does in-place conversion of Microsoft's NTFS
filesystem to the open-source filesystem Btrfs, much as btrfs-convert
does for ext2.

The original image is saved as a reflink copy at image/ntfs.img,
and if you want to keep the conversion you can delete this to
free up space.


%prep
%autosetup -p1


%build
%cmake
%cmake_build

%install
%cmake_install


%files
%license LICENCE
%doc README.md
%{_sbindir}/ntfs2btrfs
%{_mandir}/man8/ntfs2btrfs.8*


%changelog
%autochangelog
