%global git_commit e9db8d9f7486eae38f5b86531629019ad28f514e

Summary:	Pythonic Smart Contract Language for the EVM
Name:		vyper
Version:	0.4.0
Release:	%autorelease
BuildArch:	noarch
License:	Apache-2.0
URL:		https://vyperlang.org
Source0:	%{pypi_source %{name}}
Patch1:		vyper-0001-Use-Cryptodomex.patch
Patch2:		vyper-0002-Ease-version-requirements.patch
Patch3:		vyper-0003-Lark-should-go-to-the-main-install-section-as-it-use.patch
Patch4:		vyper-0004-Remove-unnecessary-shebang.patch
Patch5:		vyper-0005-Relax-lark-requirement-testing-only-anyway.patch
BuildRequires:	git
BuildRequires:	python3-devel

%description
%{summary}.

%prep
%autosetup -p1
echo %{sub %git_commit 0 7} > ./vyper/vyper_git_commithash.txt

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{name}
rm -f %{buildroot}/usr/vyper_git_commithash.txt

%check
%pyproject_check_import
# FIXME not enough dependencies
#%%pytest

%files -f %{pyproject_files}
%doc README.md SECURITY.md
%{_bindir}/fang
%{_bindir}/vyper
%{_bindir}/vyper-json

%changelog
%autochangelog
