Name:           python-rapidfuzz
Version:        3.10.0
Release:        %autorelease
Summary:        Rapid fuzzy string matching in Python and C++ using the Levenshtein Distance

License:        MIT
URL:            https://github.com/maxbachmann/RapidFuzz
Source:         %{pypi_source rapidfuzz}

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  python3-hypothesis
# Pandas will drop i686
# https://bugzilla.redhat.com/show_bug.cgi?id=2263999
BuildRequires:  (python3-pandas or python3(x86-32))
BuildRequires:  python3-pytest
# The PyPi sources don't depend on Cython since they contain pre-generated sources,
# but those are rebuilt for Fedora so Cython must be available.
BuildRequires:  python3-cython >= 3
BuildRequires:  rapidfuzz-cpp-static
BuildRequires:  taskflow-static

%global _description %{expand:
RapidFuzz is a fast string matching library for Python and C++, which is using
the string similarity calculations from FuzzyWuzzy. However there are a couple
of aspects that set RapidFuzz apart from FuzzyWuzzy:
- It is MIT licensed so it can be used whichever License you might want
to choose for your project, while you're forced to adopt the GPL license when
using FuzzyWuzzy
- It provides many string_metrics like hamming or jaro_winkler, which
are not included in FuzzyWuzzy
- It is mostly written in C++ and on top of this comes with a lot of Algorithmic
improvements to make string matching even faster, while still providing the same
results. For detailed benchmarks check the documentation
- Fixes multiple bugs in the partial_ratio implementation}

%description %_description

%package -n python3-rapidfuzz
Summary:        %{summary}

Obsoletes:      python3-rapidfuzz-devel < 3.10
Obsoletes:      python3-rapidfuzz+full < 3.10

%description -n python3-rapidfuzz %_description

%pyproject_extras_subpkg -n python3-rapidfuzz all


%prep
%autosetup -p1 -n rapidfuzz-%{version}
# External dependencies (rapidfuzz-cpp and taskflow) are removed here,
# they are already packaged in Fedora and we BuildRequire them above.
rm extern -r

# Remove pregenerated Cython sources
rm $(grep -rl '/\* Generated by Cython')


%generate_buildrequires
%pyproject_buildrequires -p -x all


%build
# Prevent build without C extensions
export RAPIDFUZZ_BUILD_EXTENSION=1

# To avoid empty debugsourcefiles.list, we need to build the package
# with RelWithDebInfo
# Upstream issue: https://github.com/scikit-build/scikit-build-core/issues/915
export SKBUILD_CMAKE_BUILD_TYPE=RelWithDebInfo
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files rapidfuzz


%check
%pytest -v


%files -n python3-rapidfuzz -f %{pyproject_files}
%doc README.*


%changelog
%autochangelog