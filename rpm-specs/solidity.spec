%global git_hash 7893614a31fbeacd1966994e310ed4f760772658

Summary:	Object-oriented, high-level language for implementing smart contracts
Name:		solidity
Version:	0.8.28
Release:	%autorelease
ExcludeArch:	%{ix86}
URL:		https://docs.soliditylang.org/
Source0:	https://github.com/ethereum/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# libsolutil/picosha2.h licensed under MIT
License:	GPL-3.0-only and MIT
# Patches no. 1-4 are Fedora-specific
Patch1:		solidity-0001-Use-system-wide-libs.patch
Patch2:		solidity-0002-Continue-on-big-endians.patch
Patch3:		solidity-0003-Use-static-linking-for-internal-libs.patch
Patch4:		solidity-0004-We-don-t-have-nlohmann-json-library-only-header.patch
# Fedora-specific
Patch5:		solidity-0005-Don-t-override-Fedora-specific-CXXFLAGS.patch
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.0
# only for Fedora 40+
BuildRequires:	cmake(fmt) >= 10.1.1
BuildRequires:	cmake(nlohmann_json)
BuildRequires:	cmake(range-v3)
BuildRequires:	cmake(z3)
BuildRequires:	cvc5
BuildRequires:	gcc-c++
BuildRequires:	help2man
# for /usr/bin/cvc5
Requires:	cvc5

%description
Solidity is an object-oriented, high-level language for implementing smart
contracts. Smart contracts are programs which govern the behavior of accounts
within the Ethereum state.

%prep
%autosetup -p1
echo %{git_hash} > commit_hash.txt

%build
%{cmake} \
	-DIGNORE_VENDORED_DEPENDENCIES:BOOL=ON \
	-DBoost_USE_STATIC_LIBS:BOOL=OFF \
	-DSTRICT_Z3_VERSION:BOOL=OFF \
	-DTESTS:BOOL=OFF
%cmake_build

help2man --no-discard-stderr --no-info "%{__cmake_builddir}/solc/solc" --version-string=%{version} --output=solc.1
help2man --no-discard-stderr --no-info "%{__cmake_builddir}/tools/yul-phaser" --version-string=%{version} --output=yul-phaser.1

%install
%cmake_install
install -D -pv -m 0644 -t %{buildroot}%{_mandir}/man1/ solc.1 yul-phaser.1

%check
# TODO

%files
%{_bindir}/solc
%{_bindir}/yul-phaser
%doc README.md
%doc SECURITY.md
%license LICENSE.txt
%{_mandir}/man1/solc.1.*
%{_mandir}/man1/yul-phaser.1.*

%changelog
%autochangelog
