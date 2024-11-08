%bcond_without check

%global srcname scikit-learn

%global _description %{expand: 
Scikit-learn integrates machine learning algorithms in the tightly-knit 
scientific Python world, building upon numpy, scipy, and matplotlib. 
As a machine-learning module, it provides versatile tools for data mining 
and analysis in any field of science and engineering. It strives to be 
simple and efficient, accessible to everybody, and reusable 
in various contexts.}

Name: python-scikit-learn
Version: 1.4.1.post1
Release: %autorelease
Summary: Machine learning in Python
# sklearn/externals/_arff.py is MIT
# sklearn/src/liblinear is BSD
# sklearn/src/libsvm is BSD
# Automatically converted from old format: BSD and MIT - review is highly recommended.
License: LicenseRef-Callaway-BSD AND LicenseRef-Callaway-MIT

URL: http://scikit-learn.org/
Source0: %{pypi_source}

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: python3-devel
BuildRequires: %{py3_dist setuptools}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

%description %_description

%package -n python3-%{srcname}
Summary: %{summary}

%if %{with check}
BuildRequires: %{py3_dist pytest} >= 7.1.2
BuildRequires: %{py3_dist joblib} >= 1.2.0
BuildRequires: %{py3_dist threadpoolctl} >= 2.0.0
%endif

%{?python_provide:%python_provide python3-sklearn}

%description -n python3-%{srcname} 
%_description

%prep
%autosetup -n %{srcname}-%{version} -p1
find sklearn/metrics/_dist_metrics.pyx.tp -type f | xargs sed -i 's/cdef inline {{INPUT_DTYPE_t}} rdist/cdef {{INPUT_DTYPE_t}} rdist/g'

%generate_buildrequires
# Some tests packages not in Fedora
%pyproject_buildrequires 

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files sklearn

%check
%if %{with check}
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_ADDOPTS='-p no:cacheprovider'
pushd %{buildroot}%{python3_sitearch}
  pytest  \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[True-liac-arff]" \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[False-liac-arff]" \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[True-pandas]" \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[False-pandas]" \
  --deselect "sklearn/covariance/tests/test_covariance.py" \
  --deselect "sklearn/covariance/tests/test_robust_covariance.py" \
  --deselect "sklearn/linear_model/tests/test_bayes.py::test_toy_ard_object" \
  --deselect "sklearn/linear_model/tests/test_bayes.py::test_ard_accuracy_on_easy_problem[42-10-100]" \
  --deselect "sklearn/linear_model/tests/test_bayes.py::test_ard_accuracy_on_easy_problem[42-100-10]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression()-check_estimators_dtypes]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression()-check_regressors_no_decision_function]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression()-check_methods_sample_order_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression()-check_methods_subset_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression()-check_dont_overwrite_parameters]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression()-check_fit2d_predict1d]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[EllipticEnvelope()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[EmpiricalCovariance()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA()-check_methods_sample_order_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA()-check_methods_subset_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA()-check_dict_unchanged]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA()-check_dont_overwrite_parameters]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA()-check_fit2d_predict1d]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[KernelPCA()-check_fit2d_1sample]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[LedoitWolf()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[MinCovDet()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[OAS()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[RidgeCV()-check_fit2d_1sample]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[RidgeClassifierCV()-check_fit2d_1sample]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ShrunkCovariance()-check_fit2d_1feature]" \
  --deselect "sklearn/utils/tests/test_validation.py::test_check_is_fitted_with_attributes[list]" \
  --deselect "sklearn/utils/tests/test_validation.py::test_check_is_fitted" \
%ifarch ppc64le
  --deselect "sklearn/tests/test_calibration.py::test_calibrated_classifier_cv_zeros_sample_weights_equivalence[True-isotonic]" \
%endif
  sklearn
popd

%else
%py3_check_import sklearn
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%doc examples/
%license COPYING sklearn/svm/src/liblinear/COPYRIGHT

%changelog
%autochangelog
