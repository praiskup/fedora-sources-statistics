Name: pass-audit
Version: 1.2
Release: %autorelease
Summary: A pass extension for auditing your password repository

%global pypkg pass_audit
%global common_name pass-audit

License: GPL-3.0-or-later
URL: https://github.com/roddhjav/%{name}
Source: https://github.com/roddhjav/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source: https://github.com/roddhjav/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
Source: https://pujol.io/keys/0xc5469996f0df68ec.asc

# https://github.com/roddhjav/pass-audit/pull/32
Patch: 0001-Install-data-files-from-the-Makefile.patch
# https://github.com/roddhjav/pass-audit/pull/33
Patch: 0001-remove-shebang-from-non-executable-__main__.py-file.patch

BuildRequires: gnupg2
BuildRequires: python3-devel
BuildRequires: make
# Test dependencies
BuildRequires: python3dist(pytest)
BuildRequires: pass

Requires: python3-%{name} = %{version}-%{release}

BuildArch: noarch

%description
`pass audit` is a password-store extension for auditing your password
repository. Passwords will be checked against the Python implementation of
Dropbox' zxcvbn algorithm and Troy Hunt's Have I Been Pwned Service. It supports
safe breached password detection from haveibeenpwned.com using a K-anonymity
method. Using this method, you do not need to (fully) trust the server that
stores the breached password. You should read the security consideration section
for more information.

%package -n python3-%{name}
Summary: %{summary}
Requires: pass

%description -n python3-%{name}
`pass audit` python package.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%check
%pytest tests

%install
%pyproject_install
%pyproject_save_files -l %{pypkg}
%make_install PYTHON=no

%files -f %{pyproject_files} -n python3-%{name}

%files
%doc README.md
%{_usr}/lib/password-store/extensions/audit.bash
%{_mandir}/man1/%{common_name}.1*
%{bash_completions_dir}/%{common_name}
%{zsh_completions_dir}/_%{common_name}

%changelog
%autochangelog
