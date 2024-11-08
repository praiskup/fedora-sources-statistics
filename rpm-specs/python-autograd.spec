Name:           python-autograd
Version:        1.7.0
Release:        %autorelease
Summary:        Efficiently computes derivatives of numpy code

%global forgeurl https://github.com/HIPS/autograd
%forgemeta

# SPDX
License:        MIT
URL:            %forgeurl
Source:         %forgesource

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-scipy

%global _description %{expand:
Autograd can automatically differentiate native Python and Numpy code. It can
handle a large subset of Python's features, including loops, ifs, recursion and
closures, and it can even take derivatives of derivatives of derivatives.  It
supports reverse-mode differentiation (a.k.a. backpropagation), which means it
can efficiently take gradients of scalar-valued functions with respect to
array-valued arguments, as well as forward-mode differentiation, and the two
can be composed arbitrarily. The main intended application of Autograd is
gradient-based optimization.}

%description %_description

%package -n python3-autograd
Summary:        %{summary}

Recommends:     python3-scipy

%description -n python3-autograd %_description

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.


%prep
%forgeautosetup -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files autograd


%check
%pyproject_check_import

# https://github.com/HIPS/autograd/issues/588#issuecomment-1479446916
k="${k-}${k+ and }not test_odeint"

%pytest -k "${k-}"


%files -n python3-autograd -f %{pyproject_files}
%license license.txt
%doc README.md


%files doc
%doc examples/
%license license.txt


%changelog
%autochangelog
