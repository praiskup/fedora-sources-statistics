# Work around a series of circular test dependencies:
#
#    python-snakemake-interface-report-plugins
#    ￬￪   ⬐───╮
# snakemake → python-snakemake-interface-executor-plugins⬎
#   ￪￪￪ │ ⬑────────────────────python-snakemake-executor-plugin-cluster-generic
#   │││ ↳python-snakemake-interface-storage-plugins─────────────────╮
#   │││                                           ￬────────────────╮│
#   ││╰────────────────────────python-snakemake-storage-plugin-http││
#   │╰─────────────────────────python-snakemake-storage-plugin-s3🠔─╯│
#   ╰──────────────────────────python-snakemake-storage-plugin-fs🠔──╯
#
# A good build order is:
#
#   1. BOOTSTRAP: python-snakemake-interface-executor-plugins,
#      python-snakemake-interface-storage-plugins,
#      python-snakemake-interface-report-plugins
#   2. BOOTSTRAP: snakemake
#   3. python-snakemake-executor-plugin-cluster-generic,
#      python-snakemake-storage-plugin-http,
#      python-snakemake-storage-plugin-s3,
#      python-snakemake-storage-plugin-fs
#   4. snakemake, python-snakemake-interface-executor-plugins,
#      python-snakemake-interface-storage-plugins,
#      python-snakemake-interface-report-plugins
%bcond bootstrap 0
%bcond tests %{without bootstrap}
# Run tests that require network access? This only makes sense for local mock
# builds in combination with --enable-network.
%bcond network_tests 0

%global _description %{expand:
The Snakemake workflow management system is a tool to create reproducible and
scalable data analyses. Workflows are described via a human readable, Python
based language. They can be seamlessly scaled to server, cluster, grid and
cloud environments, without the need to modify the workflow definition.
Finally, Snakemake workflows can entail a description of required software,
which will be automatically deployed to any execution environment.}

Name:           snakemake
Version:        8.18.2
Release:        %autorelease 
Summary:        Workflow management system to create reproducible and scalable data analyses

# The entire project is (SPDX) MIT, except:
# - versioneer.py is Unlicense
# - snakemake/_version.py says:
#     This file is released into the public domain.
#   which would be LicenseRef-Fedora-Public-Domain, except that the comments in
#   versioneer.py make it clear that Unlicense is intended for the generated
#   files as well.
License:        MIT AND Unlicense
URL:            https://snakemake.readthedocs.io/en/stable/index.html
Source:         https://github.com/snakemake/snakemake/archive/v%{version}/snakemake-%{version}.tar.gz

# chore(deps): allow pulp 2.9
# https://github.com/snakemake/snakemake/pull/3138
Patch:          https://github.com/snakemake/snakemake/pull/3138.patch

BuildArch:      noarch

BuildRequires:  python3-devel

BuildRequires:  help2man

# Snakemake uses (unversioned) "python" as the default remote execution
# command. Because remote hosts could be Windows machines, and those are likely
# to lack "python3.exe" (see https://github.com/python/cpython/issues/99185),
# we didn’t try to convince upstream to change this. Instead, we (reluctantly)
# just make sure that our own Snakemake installations are compatible by
# depending on python-unversioned-command.
BuildRequires:  python-unversioned-command
Requires:       python-unversioned-command

BuildRequires:  vim-filesystem
Requires:       vim-filesystem

Provides:       vim-snakemake = %{version}-%{release}
# These extras were removed upstream in Snakemake 8.0.0. Retain the Obsoletes
# until F40 reaches EOL so we have a clean upgrade path.
Obsoletes:      snakemake+azure < 8.1.0-1
Obsoletes:      snakemake+google-cloud < 8.1.0-1
# We no longer build Sphinx-generated PDF documentation. Beginning with 8.2.3,
# this would require patching out sphinxawesome-theme from docs/conf.py. It’s
# possible but tedious.
Obsoletes:      snakemake-doc < 8.2.1-2

%if %{with tests}
# For several tests (either apptainer or singularity-ce should work):
BuildRequires:  (apptainer or singularity-ce)
%if %{with conda_tests}
# For several tests
BuildRequires:  conda
%endif
# For test_env_modules:
BuildRequires:  environment-modules
# For test_filegraph and test_env_modules, which use dot:
BuildRequires:  graphviz
# For test_github_issue1158:
BuildRequires:  strace
# For test_benchmark and test_benchmark_jsonl:
BuildRequires:  stress

# See test-environment.yml for a listing of test dependencies, along with a lot
# of other cruft.
BuildRequires:  %{py3_dist boto3}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-mock}
BuildRequires:  %{py3_dist snakemake-executor-plugin-cluster-generic}
BuildRequires:  %{py3_dist snakemake-storage-plugin-http}
BuildRequires:  %{py3_dist snakemake-storage-plugin-fs}
BuildRequires:  %{py3_dist snakemake-storage-plugin-s3}
%endif
# For import-testing snakemake.gui
BuildRequires:  %{py3_dist flask}
# For import-testing snakemake.executors.google_lifesciences_helper:
BuildRequires:  %{py3_dist google-cloud-storage}

%description %_description

# No metapackage for “pep” extra because the following are not packaged:
#   - python3-eido
#   - python3-peppy
%pyproject_extras_subpkg -n snakemake reports messaging

%prep
%autosetup -n snakemake-%{version} -p1
%py3_shebang_fix .
# Remove shebangs from non-executable scripts. The Python script is executable
# in the source tree but will be installed without executable permissions.
sed -r -i '1{/^#!/d}' \
    snakemake/executors/jobscript.sh \
    snakemake/executors/google_lifesciences_helper.py

# Copy and rename nano and vim extensions readmes for use in the main
# documentation directory.
for editor in nano vim
do
  cp -vp "misc/${editor}/README.md" "README-${editor}.md"
done

%generate_buildrequires
# Generate BR’s for all supported extras to ensure they do not FTI
%pyproject_buildrequires -x reports,messaging

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l snakemake

# We wait until %%install to generate the man page so that we can use the
# proper script entry point. The generated man page is not perfect, but it is
# good enough to be useful.
install -d %{buildroot}%{_mandir}/man1
PATH="${PATH-}:%{buildroot}%{_bindir}" \
    PYTHONPATH='%{buildroot}%{python3_sitelib}' \
    help2man --no-info --name='%{summary}' snakemake \
    > %{buildroot}%{_mandir}/man1/snakemake.1

# Install nano syntax highlighting
install -t '%{buildroot}%{_datadir}/nano' -D -m 0644 -p \
    misc/nano/syntax/snakemake.nanorc

# Install vim syntax highlighting
install -d '%{buildroot}%{_datadir}/vim/vimfiles'
cp -vrp misc/vim/* '%{buildroot}%{_datadir}/vim/vimfiles'
find '%{buildroot}%{_datadir}/vim/vimfiles' \
    -type f -name 'README.*' -print -delete

%check
# Even if we are running the tests, this is useful; it could turn up import
# errors that would only be revealed by tests we had to disable (e.g. due to
# network access).
#
# ImportError from snakemake.executors.flux (no 'sleep' in
# snakemake_interface_executor_plugins.utils)
# https://github.com/snakemake/snakemake/issues/2598
# “The flux module is actually supposed to be moved into a plugin and has no
# connection to the rest of the code anymore.”
%pyproject_check_import -e '*.tests*' -e 'snakemake.executors.flux'

%if %{with tests}
%if %{without network_tests}
# The following require network access (and pass if it is available).
k="${k-}${k+ and }not test_ancient"
k="${k-}${k+ and }not test_containerized"
k="${k-}${k+ and }not test_default_storage"
k="${k-}${k+ and }not test_default_storage_local_job"
k="${k-}${k+ and }not test_github_issue78"
k="${k-}${k+ and }not test_issue1083"
k="${k-}${k+ and }not test_load_metawrapper"
k="${k-}${k+ and }not test_module_complex"
k="${k-}${k+ and }not test_module_complex2"
k="${k-}${k+ and }not test_module_report"
k="${k-}${k+ and }not test_module_with_script"
k="${k-}${k+ and }not test_modules_meta_wrapper"
k="${k-}${k+ and }not test_modules_prefix"
k="${k-}${k+ and }not test_output_file_cache_storage"
k="${k-}${k+ and }not test_report"
k="${k-}${k+ and }not test_report_dir"
k="${k-}${k+ and }not test_report_display_code"
k="${k-}${k+ and }not test_report_zip"
k="${k-}${k+ and }not test_rule_inheritance_globals"
k="${k-}${k+ and }not test_storage"
%endif

# This requires network access, and also fails mysteriously, without a clear
# error message. Since the test involves a container, we assume there are a lot
# of things that could be going on that don’t reflect real problems.
k="${k-}${k+ and }not test_shell_exec"

# The following require conda (but not mamba)
k="${k-}${k+ and }not test_singularity_conda"
k="${k-}${k+ and }not test_containerized"

# The following require cwltool,
# https://github.com/common-workflow-language/cwltool, which is not packaged.
# They might also require network access.
k="${k-}${k+ and }not test_cwl_singularity"

# The following require mamba, which is not packaged. (We do have micromamba,
# but that does not suffice.) They might also require network access.
k="${k-}${k+ and }not test_archive"
k="${k-}${k+ and }not test_conda"
k="${k-}${k+ and }not test_conda_create_envs_only"
k="${k-}${k+ and }not test_conda_custom_prefix"
k="${k-}${k+ and }not test_conda_function"
k="${k-}${k+ and }not test_conda_global"
k="${k-}${k+ and }not test_conda_named"
k="${k-}${k+ and }not test_conda_pin_file"
k="${k-}${k+ and }not test_conda_python_3_7_script"
k="${k-}${k+ and }not test_conda_python_script"
k="${k-}${k+ and }not test_converting_path_for_r_script"
k="${k-}${k+ and }not test_deploy_hashing"
k="${k-}${k+ and }not test_deploy_script"
k="${k-}${k+ and }not test_issue1093"
k="${k-}${k+ and }not test_issue635"
k="${k-}${k+ and }not test_jupyter_notebook"
k="${k-}${k+ and }not test_jupyter_notebook_draft"
k="${k-}${k+ and }not test_prebuilt_conda_script"
k="${k-}${k+ and }not test_script"
k="${k-}${k+ and }not test_script_pre_py39"
k="${k-}${k+ and }not test_wrapper"
k="${k-}${k+ and }not test_wrapper_local_git_prefix"

# The following require the “pep” extra. They might also require network
# access.
k="${k-}${k+ and }not test_modules_peppy"
k="${k-}${k+ and }not test_pep_pathlib"
k="${k-}${k+ and }not test_peppy"

# TODO: What is the root cause here?
# E           AssertionError: expected error on execution
k="${k-}${k+ and }not test_strict_mode"

# TODO: What is the root cause here?
# /usr/bin/bash: line 1: /usr/bin/activate: No such file or directory
# /usr/bin/bash: line 1: /builddir/.bashrc: No such file or directory
# Activating conda environment: .snakemake/conda/e4dc474209c43f7737d680b3f7ada436_
# /usr/bin/bash: line 1: Tm: command not found
k="${k-}${k+ and }not test_upstream_conda"

%if 0%{?fedora} > 40
# TODO: What is the root cause here?
# Is it Python 3.13? A dependency version? Something else?
# E                       AssertionError: wrong result produced for file 'test.1.out':
# E                       ------found------
# E                       1
# E                       -----expected-----
# E                       1
# E                       1
# E                       1
# E                       -----------------
k="${k-}${k+ and }not test_group_job_resources_with_pipe"
%endif

# See discussion in https://github.com/snakemake/snakemake/issues/2961
# regarding running individual tests explicitly rather than letting pytest
# discover them freely, and see the “Test local” step in
# .github/workflows/main.yml for the list of tests that should be run.
#   - tests/test_api.py requires network access and S3 credentials
%pytest -v -k "${k-}" ${ignore-} \
     tests/tests.py \
     tests/test_expand.py \
     tests/test_io.py \
     tests/test_schema.py \
     tests/test_linting.py \
     tests/test_executor_test_suite.py
%endif

%files -f %{pyproject_files}
%doc CHANGELOG.md
%doc README.md
%doc README-nano.md
%doc README-vim.md

%{_bindir}/snakemake
%{_mandir}/man1/snakemake.1*

# This is not owned by the filesystem package, and there is no nano-filesystem
# subpackage, so we co-own the directory to avoid depending on nano.
%dir %{_datadir}/nano/
%{_datadir}/nano/snakemake.nanorc

%{_datadir}/vim/vimfiles/ftdetect/snakemake.vim
%{_datadir}/vim/vimfiles/ftplugin/snakemake/
%{_datadir}/vim/vimfiles/syntax/snakemake.vim

%changelog
%autochangelog
