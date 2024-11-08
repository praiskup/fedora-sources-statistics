Name:           jrnl
Version:        4.1
Release:        %autorelease
Summary:        Collect your thoughts and notes without leaving the command line

License:        GPL-3.0-only
URL:            https://jrnl.sh
%global forgeurl https://github.com/jrnl-org/jrnl/
Source:         %{forgeurl}/archive/v%{version}/jrnl-%{version}.tar.gz

# Downstream-only: do not upper-bound the Python interpreter version
#
# We must integrate with new Python interpreter versions whether upstream
# is ready or not.
Patch:          0001-Downstream-only-do-not-upper-bound-the-Python-interp.patch

# Support pytest_bdd 7.1.2 and later
# https://github.com/jrnl-org/jrnl/pull/1878
Patch:          %{forgeurl}/pull/1878.patch

BuildArch:      noarch

BuildRequires:  python3-devel

BuildRequires:  dos2unix
BuildRequires:  help2man

# The mkdocs-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can package the Markdown sources without building them; they are still
# relatively legible as plain text. However, the text documentation files are
# no longer large or numerous enough to justify a separate -doc subpackage.
Obsoletes:      jrnl-doc < 3.3-1

%description
jrnl is a simple journal application for the command line.

You can use it to easily create, search, and view journal entries. Journals are
stored as human-readable plain text, and can also be encrypted using AES
encryption.


%prep
%autosetup -n jrnl-%{version} -p1

dos2unix --keepdate \
    SECURITY.md \
    docs/external-editors.md \
    docs/journal-types.md \
    docs/reference-command-line.md \
    docs/reference-config-file.md


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel

# https://github.com/jrnl-org/jrnl/issues/74
# https://github.com/jrnl-org/jrnl/issues/1274
help2man --no-info '%{python3} -m jrnl' --output='jrnl.1'


%install
%pyproject_install
%pyproject_save_files jrnl

install -D -t '%{buildroot}%{_mandir}/man1' -p -m 0644 'jrnl.1'


%check
%if v"0%{?python3_version}" >= v"3.13"
# Add Python 3.13 support
# https://github.com/jrnl-org/jrnl/issues/1893
k="${k-}${k+ and }not (TestYaml and test_export_to_nonexisting_folder)"
%endif
%tox -- -- -k "${k-}" -rs


%files -f %{pyproject_files}
%license LICENSE.md

%doc CHANGELOG.md
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc README.md
%doc SECURITY.md
%doc docs/

%{_bindir}/jrnl
%{_mandir}/man1/jrnl.1*


%changelog
%autochangelog
