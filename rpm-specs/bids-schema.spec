Name:           bids-schema
Version:        0.11.3
Release:        %autorelease
Summary:        BIDS schema description

# The specification, and the schema data derived from it, are CC-BY-4.0.
#
# The Python library in tools/schemacode/, packaged as python3-bidsschematools,
# is MIT.
License:        CC-BY-4.0
URL:            https://github.com/bids-standard/bids-specification
# The PyPI sdist corresponds to the tools/schemacode directory in git.
Source0:        %{url}/archive/schema-%{version}/bids-specification-schema-%{version}.tar.gz

# Tests would like to use the following datasets from
# https://github.com/bids-standard/bids-examples:
#   CC0-1.0:
#   - asl003/ ds000248/ micr_SEMzarr/ micr_SPIM/ pet003/ qmri_tb1tfl/
#   CC-BY-4.0:
#   - eeg_cbm/
#   Unclear licensing (no license specified or "Custom" with no text or details):
#   - hcp_example_bids/ qmri_vfa/
#   ODC-By-1.0 (not-allowed in Fedora)
#   - fnirs_automaticity/
#
# Also, the following from https://github.com/bids-standard/bids-error-examples:
#   CC0-1.0:
#   - invalid_asl003/ invalid_pet001/
#
# See BIDS_SELECTION and BIDS_ERROR_SELECTION in
# tools/schemacode/bidsschematools/conftest.py.
#
# We use the latest commits from each repository at the time of packaging; see
# tools/schemacode/bidsschematools/conftest.py, which contains code to download
# these if they are not present.
%global examples_url https://github.com/bids-standard/bids-examples
%global examples_commit 7c18d6840982518a0251cfeb59fe5c4610099ea1
%global error_examples_url https://github.com/bids-standard/bids-error-examples
%global error_examples_commit ac0a2f58f34ce284847dde5bd3b90d7ea048c141
#
# We use a script to create archives containing only the test datasets that
# fall under clearly-acceptable content license terms *and* are used in the
# tests. The script requires that each of the following macros occupies a
# single (long, if necessary) line.
%global examples asl003 ds000248 eeg_cbm micr_SEMzarr micr_SPIM pet003 qmri_tb1tfl
%global error_examples invalid_asl003 invalid_pet001
# Run this script with no arguments to parse the spec file (in the same
# directory) for commits, URLs, and whitelisted datasets, and create two
# corresponding source archives in the current working directory.
Source1:        get_test_data
# License: CC0-1.0 AND CC-BY-4.0
# (does not contribute to the licenses of the binary RPMs)
Source2:        bids-examples-%{examples_commit}-filtered.tar.zst
# License: CC0-1.0
# (does not contribute to the licenses of the binary RPMs)
Source3:        bids-error-examples-%{error_examples_commit}-filtered.tar.zst

# Man pages hand-written for Fedora in groff_man(7) format based on --help
Source10:       bst.1
Source11:       bst-export.1

BuildArch:      noarch

BuildRequires:  symlinks
BuildRequires:  python3-devel
# The tests extra includes mostly linting/coverage tools; considering
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters,
# it is easier to enumerate test dependencies by hand.
BuildRequires:  %{py3_dist pytest}

%description
Portions of the BIDS specification are defined using YAML files in order to
make the specification machine-readable.

Currently the portions of the specification that rely on this schema are:

  • the entity tables,
  • entity definitions,
  • filename templates,
  • metadata tables.

Any changes to the specification should be mirrored in the schema.


%package -n python3-bidsschematools
Summary:        Python tools for working with the BIDS schema
License:        MIT

Requires:       %{name} = %{version}-%{release}

%description -n python3-bidsschematools
A Python library (available after installation in the Python interpreter as
bidsschematools) for working with the Brain Imaging Data Structure (BIDS)
schema.

Features: 

  • lightweight
  • reference schema parsing implementation used for schema testing
  • simple CLI bindings (e.g. bst export)


%pyproject_extras_subpkg -n python3-bidsschematools render expressions


%prep
%autosetup -n bids-specification-schema-%{version}
%setup -q -T -D -a 2 -c -n bids-specification-schema-%{version}
%setup -q -T -D -a 3 -c -n bids-specification-schema-%{version}

# Remove JavaScript sources used for building the specification documents
# (which we don’t do anyway); these include a bundled pre-compiled/minified
# version of JQuery, which is (license-wise) allowable in the source RPM, but
# must not be shipped in the binary RPMs. Removing it confirms that it is not
# used or shipped. We also preemptively remove the CSS sources, which currently
# don’t contain anything bundled or pre-minified, but are unused and might
# contain something objectionable in a future release.
rm -rf src/js/ src/css/


%generate_buildrequires
pushd tools/schemacode >/dev/null
%pyproject_buildrequires -x render,expressions
popd >/dev/null


%build
pushd tools/schemacode >/dev/null
%pyproject_wheel
popd

# bst -v export --output src/schema.json


%install
# Imitate the structure of https://github.com/bids-standard/bids-schema/ in
# case we start packaging from that in the future.
install -d '%{buildroot}%{_datadir}/bids-schema/versions/%{version}'
ln -s '%{version}' '%{buildroot}%{_datadir}/bids-schema/versions/latest'
cp -rvp src/schema \
    '%{buildroot}%{_datadir}/bids-schema/versions/%{version}/schema'
# While https://github.com/bids-standard/bids-schema does not install
# metaschema.json alongside the schema/ directory, it *is* included in the PyPI
# sdist for bidsschematools.
install -t '%{buildroot}%{_datadir}/bids-schema/versions/%{version}' \
    -p -m 0644 src/metaschema.json

pushd tools/schemacode >/dev/null
%pyproject_install
%pyproject_save_files -l bidsschematools
popd

# Unbundle the schema data from the Python library.
sed -r -i '/\/bidsschematools\/data(\/|$)/d' %{pyproject_files}
rm -rvf '%{buidlroot}%{python3_sitelib}/bidsschematools/data'
# Create an absolute symlink into the buildroot and then convert it to a
# relative one; the relative symlink works both in %%check and after
# the package is actually installed
ln -s '%{buildroot}%{_datadir}/bids-schema/versions/%{version}' \
    '%{buildroot}%{python3_sitelib}/bidsschematools/data'
symlinks -c -o '%{buildroot}%{python3_sitelib}/bidsschematools/data'

# Generate and include a copy of the “exported” JSON version of the schema to
# imitate the structure of https://github.com/bids-standard/bids-schema. See
# readthedocs.yml. We do this in %%install rather than %%build because we need
# to use the generated “bst” entry point.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='%{buildroot}%{python3_sitelib}' \
    %{buildroot}%{_bindir}/bst -v export --output \
        '%{buildroot}%{_datadir}/bids-schema/versions/%{version}/schema.json'

# Do not ship the tests.
sed -r -i '/\/bidsschematools\/tests(\/|$)/d' %{pyproject_files}
sed -r -i '/bidsschematools\.tests(\.|$)/d' '%{_pyproject_modules}'
rm -rvf '%{buildroot}%{python3_sitelib}/bidsschematools/tests'

# Install the man pages
install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 \
    '%{SOURCE10}' '%{SOURCE11}'

# Install documentation. (Since we use %%doc with an absolute path for the
# README.md file in the schema directory, we must use absolute paths for all
# documentation; see
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_documentation.)
install -t '%{buildroot}%{_pkgdocdir}' -D -p -m 0644 \
    CITATION.cff
# The top-level README.md in the source tree is really for the *specification*,
# and this package is for the *schema*. We therefore form a relative symlink to
# the README.md in the schema directory (in two steps).
ln -s \
    '%{buildroot}%{_datadir}/bids-schema/versions/%{version}/schema/README.md' \
    '%{buildroot}%{_pkgdocdir}/README.md'
symlinks -c -o '%{buildroot}%{_pkgdocdir}/README.md'
install -t '%{buildroot}%{_docdir}/python3-bidsschematools' -D -p -m 0644 \
    tools/schemacode/README.md


%check
# Sanity check
verfile='%{_datadir}/bids-schema/versions/%{version}/schema/SCHEMA_VERSION'
[ '%{version}' = "$(cat "%{buildroot}${verfile}")" ]

%pyproject_check_import

# These tests require example files that were filtered out for license reasons.
k="${k-}${k+ and }not test_bids_datasets[hcp_example_bids]"
k="${k-}${k+ and }not test_bids_datasets[qmri_vfa]"
k="${k-}${k+ and }not test_bids_datasets[fnirs_automaticity]"

# Since we removed the tests from the installed package, we now link the
# example data into the original source copy of the library for testing.
ln -s "${PWD}/bids-examples-%{examples_commit}" \
    tools/schemacode/bidsschematools/tests/data/bids-examples
ln -s "${PWD}/bids-error-examples-%{error_examples_commit}" \
    tools/schemacode/bidsschematools/tests/data/bids-error-examples
# We also link the actual schema data, as unbundled and installed in the
# buildroot.
rm -rvf 'tools/schemacode/bidsschematools/data'
ln -s '%{buildroot}%{python3_sitelib}/bidsschematools/data' \
    'tools/schemacode/bidsschematools/data'
# All of this manipulation is OK here in %%check because we already built the
# wheel and installed the library to the buildroot.

%pytest -k "${k-}" -v


%files
%license LICENSE
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/CITATION.cff
# This is a symbolic link to the README.md in the schema directory:
%doc %{_pkgdocdir}/README.md

%dir %{_datadir}/bids-schema/
%dir %{_datadir}/bids-schema/versions/
# Symbolic link to the current version
%{_datadir}/bids-schema/versions/latest
%dir %{_datadir}/bids-schema/versions/%{version}/
%{_datadir}/bids-schema/versions/%{version}/metaschema.json
%{_datadir}/bids-schema/versions/%{version}/schema.json
%dir %{_datadir}/bids-schema/versions/%{version}/schema
%doc %{_datadir}/bids-schema/versions/%{version}/schema/README.md
# Version files
%{_datadir}/bids-schema/versions/%{version}/schema/BIDS_VERSION
%{_datadir}/bids-schema/versions/%{version}/schema/SCHEMA_VERSION
# Directories (or directory trees) filled with YAML files
%{_datadir}/bids-schema/versions/%{version}/schema/meta/
%{_datadir}/bids-schema/versions/%{version}/schema/objects/
%{_datadir}/bids-schema/versions/%{version}/schema/rules/


%files -n python3-bidsschematools -f %{pyproject_files}
%doc %dir %{_docdir}/python3-bidsschematools
%doc %{_docdir}/python3-bidsschematools/README.md

# Symbolic link to the schema data in the base package:
%{python3_sitelib}/bidsschematools/data

%{_bindir}/bst
%{_mandir}/man1/bst.1*
%{_mandir}/man1/bst-*.1*


%changelog
%autochangelog
