# See eachdist.ini:
%global stable_version 1.27.0
%global prerel_version 0.48~b0
# WARNING: Because python-opentelemetry-contrib has some exact-version
# dependencies on subpackages of this package, it must be updated
# simultaneously with this package, preferably using a side tag, such that its
# stable_version and prerel_version always match those above.

# Contents of python3-opentelemetry-proto are generated from proto files in a
# separate repository with a separate version number. We treat these as
# generated sources: we aren’t required by the guidelines to re-generate them
# (although we *may*), and it is not trival to do so, but we must still include
# the original sources.
#
# See PROTO_REPO_BRANCH_OR_COMMIT in scripts/proto_codegen.sh for the correct
# version number.
%global proto_version 1.2.0
# Similarly, various files within python3-opentelemetry-semantic-conventions
# are generated from schemas that we should, strictly speaking, also include in
# the source RPM even though it is impractical to actually re-generate sources
# with them during the build.
#
# See SEMCONV_VERSION in scripts/semconv/generate.sh for the correct version
# number. This should normally match the package’s stable version.
%global semconv_version %{stable_version}

# Unfortunately, we cannot disable the prerelease packages without breaking
# almost all of the stable packages, because opentelemetry-sdk depends on the
# prerelease package opentelementry-semantic-conventions.
%bcond prerelease 1

# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond doc_pdf 1

# The python-opencensus package was retired, so we cannot supply the
# python3-opentelemetry-opencensus-shim subpackage.
%bcond opencensus 0
# The python-opentracing package was orphaned and is expected to be retired, so
# we cannot supply the python3-opentelemetry-opentracing-shim subpackage.
%bcond opentracing 0

# Is protobuf v4 (22.x, 23.x, etc.)?
# The opentelemetry-exporter-opencensus support only protobuf v3.
%bcond protobuf4 0

# Can we depend on grpcio?
%bcond grpc 1

Name:           python-opentelemetry
Version:        %{stable_version}
Release:        %autorelease
Summary:        OpenTelemetry Python API and SDK

License:        Apache-2.0
URL:            https://github.com/open-telemetry/opentelemetry-python
Source0:        %{url}/archive/v%{version}/opentelemetry-python-%{version}.tar.gz
# Note that we do not currently use this source, but it contains the original
# .proto files for python3-opentelemetry-proto, so we must include it.
%global proto_url https://github.com/open-telemetry/opentelemetry-proto
Source1:        %{proto_url}/archive/v%{proto_version}/opentelemetry-proto-%{proto_version}.tar.gz
# Note that we do not currently use this source, but it contains the original
# schema files for python3-opentelemetry-semantic-conventions, so we must
# include it.
%global semconv_url https://github.com/open-telemetry/semantic-conventions
Source2:        %{semconv_url}/archive/v%{semconv_version}/semantic-conventions-%{semconv_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  tomcli

%if %{with doc_pdf}
BuildRequires:  make
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk

# docs-requirements.txt
BuildRequires:  %{py3_dist sphinx}
# No need for sphinx-rtd-theme since we don’t build HTML
BuildRequires:  %{py3_dist sphinx-autodoc-typehints}
# No need for sphinx-jekyll-builder since we don’t build HTML/website
# Needed for examples (and for documentation about examples):
BuildRequires:  %{py3_dist django}
%endif


%global stable_distinfo %(echo '%{stable_version}' | tr -d '~^').dist-info
# See eachdist.ini:
%global stable_pkgdirs %{shrink:
      opentelemetry-api
      opentelemetry-sdk
      opentelemetry-proto
      propagator/opentelemetry-propagator-jaeger
      propagator/opentelemetry-propagator-b3
      %{?!with_protobuf4:exporter/opentelemetry-exporter-zipkin-proto-http}
      exporter/opentelemetry-exporter-zipkin-json
      %{?!with_protobuf4:exporter/opentelemetry-exporter-zipkin}
      exporter/opentelemetry-exporter-prometheus
      %{?with_grpc:exporter/opentelemetry-exporter-otlp}
      exporter/opentelemetry-exporter-otlp-proto-common
      %{?with_grpc:exporter/opentelemetry-exporter-otlp-proto-grpc}
      exporter/opentelemetry-exporter-otlp-proto-http}
%global prerel_distinfo %(echo '%{prerel_version}' | tr -d '~^').dist-info
# See eachdist.ini:
%global prerel_pkgdirs %{shrink:
      tests/opentelemetry-test-utils
      %{?with_grpc:%{?!with_protobuf4:exporter/opentelemetry-exporter-opencensus}}
      %{?with_grpc:%{?with_opencensus:shim/opentelemetry-opencensus-shim}}
      %{?with_opentracing:shim/opentelemetry-opentracing-shim}
      opentelemetry-semantic-conventions}

%global common_description %{expand:
OpenTelemetry Python API and SDK.}

%description
%{common_description}


%if %{with prerelease} && %{without protobuf4} && %{with grpc}
%package -n python3-opentelemetry-exporter-opencensus
Summary:        OpenCensus Exporter
Version:        %{prerel_version}

Obsoletes:      python3-opentelemetry-ext-opencensusexporter < 1.0-1

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-opencensus
This library allows to export traces using OpenCensus.
%endif


%package -n python3-opentelemetry-exporter-otlp-proto-common
Summary:        OpenTelemetry Protobuf Encoding
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-proto = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-otlp-proto-common
This library is provided as a convenience to encode to Protobuf. Currently used
by:

%if %{with grpc}
  • opentelemetry-exporter-otlp-proto-grpc
%endif
  • opentelemetry-exporter-otlp-proto-http


%if %{with grpc}
%package -n python3-opentelemetry-exporter-otlp-proto-grpc
Summary:        OpenTelemetry Collector Protobuf over gRPC Exporter
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}
Requires:       python3-opentelemetry-proto = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-otlp-proto-common = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-otlp-proto-grpc
This library allows to export data to the OpenTelemetry Collector using the
OpenTelemetry Protocol using Protobuf over gRPC.
%endif


%package -n python3-opentelemetry-exporter-otlp-proto-http
Summary:        OpenTelemetry Collector Protobuf over HTTP Exporter
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}
Requires:       python3-opentelemetry-proto = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-otlp-proto-common = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-otlp-proto-http
This library allows to export data to the OpenTelemetry Collector using the
OpenTelemetry Protocol using Protobuf over HTTP.


%if %{with grpc}
%package -n python3-opentelemetry-exporter-otlp
Summary:        OpenTelemetry Collector Exporters
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-exporter-otlp-proto-grpc = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-otlp-proto-http = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-otlp
This library is provided as a convenience to install all supported
OpenTelemetry Collector Exporters. Currently it installs:

  • opentelemetry-exporter-otlp-proto-grpc
  • opentelemetry-exporter-otlp-proto-http

In the future, additional packages will be available:

  • opentelemetry-exporter-otlp-json-http

To avoid unnecessary dependencies, users should install the specific package
once they’ve determined their preferred serialization and protocol method.
%endif


%package -n python3-opentelemetry-exporter-prometheus
Summary:        OpenTelemetry Prometheus Exporter
Version:        %{prerel_version}

Obsoletes:      python3-opentelemetry-ext-prometheus < 1.0-1

Requires:       ((%{py3_dist prometheus_client} >= 0.5) with (%{py3_dist prometheus_client} < 1))
# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-prometheus
This library allows to export metrics data to Prometheus
(https://prometheus.io).


%package -n python3-opentelemetry-exporter-zipkin-json
Summary:        Zipkin Span JSON Exporter for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-zipkin-json
This library allows export of tracing data to Zipkin (https://zipkin.io/) using
JSON for serialization.


%if %{without protobuf4}
%package -n python3-opentelemetry-exporter-zipkin-proto-http
Summary:        Zipkin Span Protobuf Exporter for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-zipkin-json = %{stable_version}-%{release}

%description -n python3-opentelemetry-exporter-zipkin-proto-http
This library allows export of tracing data to Zipkin (https://zipkin.io/) using
Protobuf for serialization.
%endif


%if %{without protobuf4}
%package -n python3-opentelemetry-exporter-zipkin
Summary:        Zipkin Span Exporters for OpenTelemetry
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-exporter-zipkin-json = %{stable_version}-%{release}
Requires:       python3-opentelemetry-exporter-zipkin-proto-http = %{stable_version}-%{release}

Obsoletes:      python3-opentelemetry-ext-wsgi < 1.0-1

%description -n python3-opentelemetry-exporter-zipkin
This library is provided as a convenience to install all supported
OpenTelemetry Zipkin Exporters. Currently it installs:
  • opentelemetry-exporter-zipkin-json
  • opentelemetry-exporter-zipkin-proto-http

In the future, additional packages may be available:
  • opentelemetry-exporter-zipkin-thrift

To avoid unnecessary dependencies, users should install the specific package
once they've determined their preferred serialization method.
%endif


%package -n python3-opentelemetry-api
Summary:        OpenTelemetry Python API
Version:        %{stable_version}

# Note that the huge number of instrumentation packages are released in
# https://github.com/open-telemetry/opentelemetry-python-contrib and are
# packaged (where possible based on available dependencies) in
# https://src.fedoraproject.org/rpms/python-opentelemetry-contrib.
#
# The base opentelemetry-instrumentation package was also moved to “contrib” in
# release 1.6.1/0.25~b1. We therefore obsolete it…
Obsoletes:      python3-opentelemetry-instrumentation < 0.25~b1.1
# …and its pre-1.0 name…
Obsoletes:      python3-opentelemetry-auto-instrumentation < 1.0-1
# …and the pre-1.0 packages it was obsoleting. (Most of these are
# instrumentation extensions.)

# These have all been renamed and are now part of opentelemetry-python-contrib.
# They have a prerelease version number, which is less than the version number
# of the old packages, so obsoleting by version number alone is insufficient.
# It is fortunate, then, that they also have new names, and it is unlikely the
# old names will ever come back in any form.
#
# Any renamed pre-1.0 packages that remain in this repository are instead
# obsoleted by the corresponding new packages.

#   • opentelemetry-instrumentation-aiohttp-client
Obsoletes:      python3-opentelemetry-ext-aiohttp-client < 1.0-1
#   • opentelemetry-instrumentation-asgi
Obsoletes:      python3-opentelemetry-ext-asgi < 1.0-1
#   • opentelemetry-instrumentation-dbapi
Obsoletes:      python3-opentelemetry-ext-dbapi < 1.0-1
#   • opentelemetry-instrumentation-django
Obsoletes:      python3-opentelemetry-ext-django < 1.0-1
#   • opentelemetry-instrumentation-flask
Obsoletes:      python3-opentelemetry-ext-flask < 1.0-1
#   • opentelemetry-instrumentation-grpc
Obsoletes:      python3-opentelemetry-ext-grpc < 1.0-1
#   • opentelemetry-instrumentation-jinja2
Obsoletes:      python3-opentelemetry-ext-jinja2 < 1.0-1
#   • opentelemetry-instrumentation-mysql
Obsoletes:      python3-opentelemetry-ext-mysql < 1.0-1
#   • opentelemetry-instrumentation-psycopg2
Obsoletes:      python3-opentelemetry-ext-psycopg2 < 1.0-1
#   • opentelemetry-instrumentation-pymongo
Obsoletes:      python3-opentelemetry-ext-pymongo < 1.0-1
#   • opentelemetry-instrumentation-pymysql
Obsoletes:      python3-opentelemetry-ext-pymysql < 1.0-1
#   • opentelemetry-instrumentation-redis
Obsoletes:      python3-opentelemetry-ext-redis < 1.0-1
#   • opentelemetry-instrumentation-requests
Obsoletes:      python3-opentelemetry-ext-requests < 1.0-1
#   • opentelemetry-instrumentation-sqlalchemy
Obsoletes:      python3-opentelemetry-ext-sqlalchemy < 1.0-1
#   • opentelemetry-instrumentation-sqlite3
Obsoletes:      python3-opentelemetry-ext-sqlite3 < 1.0-1
#   • opentelemetry-instrumentation-wsgi
Obsoletes:      python3-opentelemetry-ext-wsgi < 1.0-1

#   • opentelemetry-exporter-datadog
Obsoletes:      python3-opentelemetry-ext-datadog < 1.0-1
#   • opentelemetry-exporter-jaeger (removed in 1.22.0)
Obsoletes:      python3-opentelemetry-ext-jaeger < 1.0-1

# The opentelemetry-distro package was moved to “contrib” in release
# 1.6.1/0.25~b1.
Obsoletes:      python3-opentelemetry-distro < 0.25~b1.1
Obsoletes:      python3-opentelemetry-distro+otlp < 0.25~b1.1

# These were first deprecated, then finally removed in 1.22.0.
Obsoletes:      python3-opentelemetry-exporter-jaeger-proto-grpc < 1.22.0-1
Obsoletes:      python3-opentelemetry-exporter-jaeger-thrift < 1.22.0-1
Obsoletes:      python3-opentelemetry-exporter-jaeger < 1.22.0-1

%if %{without opentracing}
# The python-opentracing package was orphaned, and is expected to be retired,
# for Fedora 42.
Obsoletes:      python3-opentelemetry-opentracing-shim < %{version}-%{release}
%endif

# If we actually disable the grpc bcond by default, we should Obsolete with a
# fixed version and release.
%if %{without grpc}
Obsoletes:      python3-opentelemetry-exporter-otlp < %{version}-%{release}
Obsoletes:      python3-opentelemetry-exporter-otlp-proto-grpc < %{version}-%{release}
%endif
%if %{without grpc} || %{with protobuf4}
Obsoletes:      python3-opentelemetry-exporter-opencensus < 0.47~b0-2
%endif

%description -n python3-opentelemetry-api
%{summary}.


%package -n python3-opentelemetry-proto
Summary:        OpenTelemetry Python Proto
Version:        %{stable_version}

%description -n python3-opentelemetry-proto
%{summary}.


%package -n python3-opentelemetry-sdk
Summary:        OpenTelemetry Python SDK
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-semantic-conventions = %{prerel_version}-%{release}

%description -n python3-opentelemetry-sdk
%{summary}.


%if %{with prerelease}
%package -n python3-opentelemetry-semantic-conventions
Summary:        OpenTelemetry Python Semantic Conventions
Version:        %{prerel_version}

%description -n python3-opentelemetry-semantic-conventions
This library contains generated code for the semantic conventions defined by
the OpenTelemetry specification.
%endif


%package -n python3-opentelemetry-propagator-b3
Summary:        OpenTelemetry B3 Propagator
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}

%description -n python3-opentelemetry-propagator-b3
This library provides a propagator for the B3 format.


%package -n python3-opentelemetry-propagator-jaeger
Summary:        OpenTelemetry Jaeger Propagator
Version:        %{stable_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}

%description -n python3-opentelemetry-propagator-jaeger
This library provides a propagator for the Jaeger format.


%if %{with prerelease} && %{with opencensus} && %{with grpc}
%package -n python3-opentelemetry-opencensus-shim
Summary:        OpenCensus Shim for OpenTelemetry
Version:        %{prerel_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}

%description -n python3-opentelemetry-opencensus-shim
%{summary}.
%endif


%if %{with prerelease} && %{with opentracing}
%package -n python3-opentelemetry-opentracing-shim
Summary:        OpenTracing Shim for OpenTelemetry
Version:        %{prerel_version}

Obsoletes:      python3-opentelemetry-ext-opentracing-shim < 1.0-1

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}

%description -n python3-opentelemetry-opentracing-shim
%{summary}.
%endif


%if %{with prerelease}
%package -n python3-opentelemetry-test-utils
Summary:        OpenTracing Test Utilities
Version:        %{prerel_version}

# Dependencies across subpackages should be fully-versioned.
Requires:       python3-opentelemetry-api = %{stable_version}-%{release}
Requires:       python3-opentelemetry-sdk = %{stable_version}-%{release}

# Subpackage was renamed upstream
Obsoletes:      python3-opentelemetry-test < 0.26~b1-1

%description -n python3-opentelemetry-test-utils
This package provides internal testing utilities for the OpenTelemetry Python
project and provides no stability or quality guarantees. Please do not use it
for anything other than writing or running tests for the OpenTelemetry Python
project (github.com/open-telemetry/opentelemetry-python).
%endif


%package doc
Summary:        Documentation and examples for python-opentelemetry
Version:        %{stable_version}

%description doc
This package provides documentation and examples for python-opentelemetry.


%prep
%autosetup -n opentelemetry-python-%{stable_version} -p1

%py3_shebang_fix docs/examples tests

# Fix a test that shells out to the unversioned Python command. This is OK
# upstream, but not in Fedora.
sed -r -i 's|shutil\.which\("python"\)|"%{python3}"|' \
    opentelemetry-sdk/tests/trace/test_trace.py

# Drop intersphinx mappings, since we can’t download remote inventories and
# can’t easily produce working hyperlinks from inventories in local
# documentation packages.
echo 'intersphinx_mapping.clear()' >> docs/conf.py

# See tox.ini. We can’t generate BuildRequires directly from tox environments
# because the top-level tox.ini is not associated with a particalar Python
# package. Upstream uses different test-requirements-#.txt files to support
# multiple tox environments for some packages, primarily to support different
# test dependencies on different Python interpreter versions or to test with
# several supported major versions of a dependency. For each package with
# multiple test-requirements-#.txt files, we select the one corresponding to
# the dependency and/or Python interpreter version we have packaged and create
# a test-requirements.txt symbolic link, which we will use for generating
# BuildRequires.
while read -r n pkg
do
  ln -s "test-requirements-${n}.txt" "${pkg}/test-requirements.txt"
done < <(sed -r '/^(#|$)/d' <<'EOF'
# 0: proto3, 1: proto4
%{with protobuf4} exporter/opentelemetry-exporter-otlp-proto-common
%{with protobuf4} exporter/opentelemetry-exporter-otlp-proto-grpc
%{with protobuf4} exporter/opentelemetry-exporter-otlp-proto-http
%{with protobuf4} opentelemetry-proto
EOF
)

for pkgdir in %{?with_prerelease:%{prerel_pkgdirs}} %{stable_pkgdirs}
do
  # Filter test requirements files so we can use them to generate
  # BuildRequires.
  #   - Convert exact-version dependencies to lower-bounds
  #   - Drop "-e" directives (unsupported, and we will generate them one way or
  #     another since we are generating BuildRequires from all packages)
  sed -r \
      -e 's/==.*//' \
      -e '/^-e /d' \
      "${pkgdir}/test-requirements.txt" > \
    "${pkgdir}/test-requirements-filtered.txt"

  skiptests=0
  case "${pkgdir}" in
  # This is currently just a placeholder in case we need it later.
  esac
  if [ "${skiptests}" != '0' ]
  then
    # Can’t run the tests (missing dependencies, everything requires network
    # access, etc.); do an import-only “smoke test” instead, and filter out
    # *all* test dependencies.
    sed -r -i 's/^/# /' "${pkgdir}/test-requirements-filtered.txt"
  fi

  # We generate BuildRequires from the per-package
  # test-requirements-filtered.txt files. This amalgamated
  # test-requirements-all.txt file is just to make debugging a little easier.
  echo "### ${pkgdir} ###" >> test-requirements-all.txt
  tee -a test-requirements-all.txt < "${pkgdir}/test-requirements-filtered.txt"
done

# Allow newer importlib_metadata
# https://github.com/open-telemetry/opentelemetry-python/issues/3570
sed -i 's/"\(importlib-metadata >= 6.0\), <= .*"/"\1"/' opentelemetry-api/pyproject.toml

%generate_buildrequires
for pkgdir in %{?with_prerelease:%{prerel_pkgdirs}} %{stable_pkgdirs}
do
  pushd "${pkgdir}" >/dev/null
  (
    %pyproject_buildrequires test-requirements-filtered.txt
    # Use grep to omit dependencies on packages that are part of
    # python-opentelemetry-contrib to avoid generating circular dependencies on
    # this package. We could filter these out of the
    # test-requirements-filtered.txt files where they appear, but we would
    # still have some (correct) runtime (inter)dependencies from the
    # pyproject.toml files.
  ) | grep -v -E '\bopentelemetry-'
  popd >/dev/null
done


%build
for pkgdir in %{?with_prerelease:%{prerel_pkgdirs}} %{stable_pkgdirs}
do
  pushd "${pkgdir}"
  %pyproject_wheel
  popd
done

# Build documentation
%if %{with doc_pdf}
PYTHONPATH="${PWD}/build/lib" %make_build -C docs latex \
    SPHINXOPTS='-j%{?_smp_build_ncpus}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif


%install
%pyproject_install


%check
for pkgdir in %{?with_prerelease:%{prerel_pkgdirs}} %{stable_pkgdirs}
do
  unset k
  case "${pkgdir}" in
  exporter/opentelemetry-exporter-otlp-proto-grpc)
    # E       AssertionError: <MetricExportResult.FAILURE: 1> !=
    #                         <MetricExportResult.SUCCESS: 0>
    # Could not reproduce in a virtualenv, and the root cause is not
    # understood, so this was not reported upstream.
    k="${k-}${k+ and }not (TestOTLPMetricExporter and test_shutdown)"
    k="${k-}${k+ and }not (TestOTLPSpanExporter and test_shutdown)"
    k="${k-}${k+ and }not (TestOTLPMetricExporter and test_success)"
    k="${k-}${k+ and }not (TestOTLPSpanExporter and test_success)"
    k="${k-}${k+ and }not (TestOTLPLogExporter and test_success)"

    # These are probably just brittle with respect to timing.
    # E           AssertionError: expected call not found.
    # E           Expected: sleep(4)
    # E             Actual: sleep(1)
    k="${k-}${k+ and }not (TestOTLPMetricExporter and test_unavailable_delay)"
    k="${k-}${k+ and }not (TestOTLPSpanExporter and test_unavailable_delay)"
    k="${k-}${k+ and }not (TestOTLPLogExporter and test_unavailable_delay)"
    # E           AssertionError: Expected 'sleep' to not have been called. Called 1 times.
    # E           Calls: [call(1)].
    k="${k-}${k+ and }not (TestOTLPMetricExporter and test_unknown_logs)"
    ;;
  exporter/opentelemetry-exporter-zipkin-proto-http)
    # These also seem to be timing issues, combined with output from different
    # streams apparently being mixed together. It would be good to report this
    # upstream, but we are not sure exactly how to usefully explain the
    # problem.  We have only seen these fail with pytest 8, but we suspect this
    # is merely a coincidence.
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_local_endpoint_default)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_local_endpoint_explicits)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_max_tag_length_10)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_max_tag_length_11)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_max_tag_length_128)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_max_tag_length_2)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_max_tag_length_5)"
    k="${k-}${k+ and }not (TestProtobufEncoder and test_encode_max_tag_length_9)"
    ;;
  exporter/opentelemetry-exporter-zipkin-json)
    # Same comments as exporter/opentelemetry-exporter-zipkin-proto-http, above:
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_local_endpoint_default)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_local_endpoint_explicits)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_max_tag_length_10)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_max_tag_length_11)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_max_tag_length_128)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_max_tag_length_2)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_max_tag_length_5)"
    k="${k-}${k+ and }not (TestV1JsonEncoder and test_encode_max_tag_length_9)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_id_zero_padding)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_local_endpoint_default)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_local_endpoint_explicits)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_max_tag_length_10)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_max_tag_length_11)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_max_tag_length_128)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_max_tag_length_2)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_max_tag_length_5)"
    k="${k-}${k+ and }not (TestV2JsonEncoder and test_encode_max_tag_length_9)"
    ;;
  esac

  %pytest "${pkgdir}" --ignore-glob='*/benchmarks/*' ${ignore-} -k "${k-}"
done


%if %{with prerelease} && %{without protobuf4} && %{with grpc}
%files -n python3-opentelemetry-exporter-opencensus
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-opencensus/LICENSE
%doc exporter/opentelemetry-exporter-opencensus/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/

%{python3_sitelib}/opentelemetry/exporter/opencensus/
%{python3_sitelib}/opentelemetry_exporter_opencensus-%{prerel_distinfo}/
%endif


%files -n python3-opentelemetry-exporter-otlp-proto-common
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-otlp-proto-common/LICENSE
%doc exporter/opentelemetry-exporter-otlp-proto-common/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/
%if %{with grpc}
%{python3_sitelib}/opentelemetry/exporter/otlp/py.typed
%endif
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/proto/

%{python3_sitelib}/opentelemetry/exporter/otlp/proto/common/
%{python3_sitelib}/opentelemetry_exporter_otlp_proto_common-%{stable_distinfo}/


%if %{with grpc}
%files -n python3-opentelemetry-exporter-otlp-proto-grpc
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-otlp-proto-grpc/LICENSE
%doc exporter/opentelemetry-exporter-otlp-proto-grpc/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/
%{python3_sitelib}/opentelemetry/exporter/otlp/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/proto/

%{python3_sitelib}/opentelemetry/exporter/otlp/proto/grpc/
%{python3_sitelib}/opentelemetry_exporter_otlp_proto_grpc-%{stable_distinfo}/
%endif


%files -n python3-opentelemetry-exporter-otlp-proto-http
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-otlp-proto-http/LICENSE
%doc exporter/opentelemetry-exporter-otlp-proto-http/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/
%dir %{python3_sitelib}/opentelemetry/exporter/otlp/proto/
%if %{with grpc}
%{python3_sitelib}/opentelemetry/exporter/otlp/py.typed
%endif

%{python3_sitelib}/opentelemetry/exporter/otlp/proto/http/
%{python3_sitelib}/opentelemetry_exporter_otlp_proto_http-%{stable_distinfo}/


%if %{with grpc}
%files -n python3-opentelemetry-exporter-otlp
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-otlp/LICENSE
%doc exporter/opentelemetry-exporter-otlp/README.rst

# Shared namespace directories are already (co)-owned by the implementation
# subpackages (-proto-grpc, -proto-http) upon which this subpackage depends.

%dir %{python3_sitelib}/opentelemetry/exporter/otlp/__pycache__/
%pycached %{python3_sitelib}/opentelemetry/exporter/otlp/version.py
%{python3_sitelib}/opentelemetry_exporter_otlp-%{stable_distinfo}/
%endif


%files -n python3-opentelemetry-exporter-prometheus
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-prometheus/LICENSE
%doc exporter/opentelemetry-exporter-prometheus/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/

%{python3_sitelib}/opentelemetry/exporter/prometheus/
%{python3_sitelib}/opentelemetry_exporter_prometheus-%{prerel_distinfo}/


%files -n python3-opentelemetry-exporter-zipkin-json
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-zipkin-json/LICENSE
# Not packaged since it is a zero-length file:
#doc exporter/opentelemetry-exporter-zipkin-json/CHANGELOG.md
%doc exporter/opentelemetry-exporter-zipkin-json/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/
%dir %{python3_sitelib}/opentelemetry/exporter/zipkin/
%{python3_sitelib}/opentelemetry/exporter/zipkin/py.typed

%{python3_sitelib}/opentelemetry/exporter/zipkin/encoder/
%{python3_sitelib}/opentelemetry/exporter/zipkin/json/
%pycached %{python3_sitelib}/opentelemetry/exporter/zipkin/node_endpoint.py
%{python3_sitelib}/opentelemetry_exporter_zipkin_json-%{stable_distinfo}/


%if %{without protobuf4}
%files -n python3-opentelemetry-exporter-zipkin-proto-http
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-zipkin-proto-http/LICENSE
# Not packaged since it is a zero-length file:
#doc exporter/opentelemetry-exporter-zipkin-proto-http/CHANGELOG.md
%doc exporter/opentelemetry-exporter-zipkin-proto-http/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/
%dir %{python3_sitelib}/opentelemetry/exporter/zipkin/
%{python3_sitelib}/opentelemetry/exporter/zipkin/py.typed
%dir %{python3_sitelib}/opentelemetry/exporter/zipkin/proto/

%{python3_sitelib}/opentelemetry/exporter/zipkin/proto/http/
%{python3_sitelib}/opentelemetry_exporter_zipkin_proto_http-%{stable_distinfo}/
%endif


%if %{without protobuf4}
%files -n python3-opentelemetry-exporter-zipkin
# Note that the contents are identical to the top-level LICENSE file.
%license exporter/opentelemetry-exporter-zipkin/LICENSE
%doc exporter/opentelemetry-exporter-zipkin/README.rst

# Shared namespace directories are already (co)-owned by the implementation
# subpackages (-json, -proto-http) upon which this subpackage depends.

%dir %{python3_sitelib}/opentelemetry/exporter/zipkin/__pycache__/
%pycached %{python3_sitelib}/opentelemetry/exporter/zipkin/version.py
%{python3_sitelib}/opentelemetry_exporter_zipkin-%{stable_distinfo}/
%endif


%files -n python3-opentelemetry-api
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-api/LICENSE
%doc opentelemetry-api/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/propagators/
%{python3_sitelib}/opentelemetry/propagators/py.typed

%{python3_sitelib}/opentelemetry/_events/
%{python3_sitelib}/opentelemetry/_logs/
%{python3_sitelib}/opentelemetry/attributes/
%{python3_sitelib}/opentelemetry/baggage/
%{python3_sitelib}/opentelemetry/context/
%{python3_sitelib}/opentelemetry/environment_variables/
%{python3_sitelib}/opentelemetry/metrics/
%{python3_sitelib}/opentelemetry/propagate/
%dir %{python3_sitelib}/opentelemetry/propagators/__pycache__/
%pycached %{python3_sitelib}/opentelemetry/propagators/composite.py
%pycached %{python3_sitelib}/opentelemetry/propagators/textmap.py
%{python3_sitelib}/opentelemetry/trace/
%{python3_sitelib}/opentelemetry/util/
%{python3_sitelib}/opentelemetry/version/
%{python3_sitelib}/opentelemetry_api-%{stable_distinfo}/


%files -n python3-opentelemetry-proto
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-proto/LICENSE
%doc opentelemetry-proto/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/proto/
%{python3_sitelib}/opentelemetry_proto-%{stable_distinfo}/


%files -n python3-opentelemetry-sdk
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-sdk/LICENSE
%doc opentelemetry-sdk/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/sdk/
%{python3_sitelib}/opentelemetry_sdk-%{stable_distinfo}/


%if %{with prerelease}
%files -n python3-opentelemetry-semantic-conventions
# Note that the contents are identical to the top-level LICENSE file.
%license opentelemetry-sdk/LICENSE
%doc opentelemetry-sdk/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/semconv/
%{python3_sitelib}/opentelemetry_semantic_conventions-%{prerel_distinfo}/
%endif


%files -n python3-opentelemetry-propagator-b3
# Note that the contents are identical to the top-level LICENSE file.
%license propagator/opentelemetry-propagator-b3/LICENSE
%doc propagator/opentelemetry-propagator-b3/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/propagators/
%{python3_sitelib}/opentelemetry/propagators/py.typed

%{python3_sitelib}/opentelemetry/propagators/b3/
%{python3_sitelib}/opentelemetry_propagator_b3-%{stable_distinfo}/


%files -n python3-opentelemetry-propagator-jaeger
# Note that the contents are identical to the top-level LICENSE file.
%license propagator/opentelemetry-propagator-jaeger/LICENSE
%doc propagator/opentelemetry-propagator-jaeger/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/propagators/
%{python3_sitelib}/opentelemetry/propagators/py.typed

%{python3_sitelib}/opentelemetry/propagators/jaeger/
%{python3_sitelib}/opentelemetry_propagator_jaeger-%{stable_distinfo}/


%if %{with prerelease} && %{with opencensus} && %{with grpc}
%files -n python3-opentelemetry-opencensus-shim
# Note that the contents are identical to the top-level LICENSE file.
%license shim/opentelemetry-opencensus-shim/LICENSE
%doc shim/opentelemetry-opencensus-shim/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/shim/

%{python3_sitelib}/opentelemetry/shim/opencensus_shim/
%{python3_sitelib}/opentelemetry_opencensus_shim-%{prerel_distinfo}/
%endif


%if %{with prerelease} && %{with opentracing}
%files -n python3-opentelemetry-opentracing-shim
# Note that the contents are identical to the top-level LICENSE file.
%license shim/opentelemetry-opentracing-shim/LICENSE
%doc shim/opentelemetry-opentracing-shim/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed
%dir %{python3_sitelib}/opentelemetry/shim/

%{python3_sitelib}/opentelemetry/shim/opentracing_shim/
%{python3_sitelib}/opentelemetry_opentracing_shim-%{prerel_distinfo}/
%endif


%if %{with prerelease}
%files -n python3-opentelemetry-test-utils
%license LICENSE
%doc tests/opentelemetry-test-utils/README.rst

# Shared namespace directories
%dir %{python3_sitelib}/opentelemetry/
%{python3_sitelib}/opentelemetry/py.typed

%{python3_sitelib}/opentelemetry/test/
%{python3_sitelib}/opentelemetry_test_utils-%{prerel_distinfo}/
%endif


%files doc
%license LICENSE
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%doc rationale.md
%doc README.md
%doc docs/examples/
%if %{with doc_pdf}
%doc docs/_build/latex/opentelemetrypython.pdf
%endif


%changelog
%autochangelog
