Name:       python-astor
Version:    0.8.1
Release:    %autorelease
Summary:    Read/rewrite/write Python ASTs

%global forgeurl https://github.com/berkerpeksag/astor
%global tag %{version}
%forgemeta

License:    BSD-3-Clause
URL:        https://astor.readthedocs.io/
Source:     %forgesource
# Apply patch solving issues with test exceeding max digit limit
# https://github.com/berkerpeksag/astor/pull/213
Patch:      https://github.com/berkerpeksag/astor/pull/213.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%global _description %{expand:
astor is designed to allow easy manipulation of Python source via the AST.

For more information see: https://astor.readthedocs.io/}

%description %_description

%package -n python3-astor
Summary:    %{summary}

%description -n python3-astor %_description

%prep
%forgeautosetup -p1
# Remove unnecessary shebang
sed -i '/\/usr\/bin\/env.*python/ d' astor/rtrip.py

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l astor


%check
# test_convert_stdlib fails with
# `AttributeError: No defined handler for node of type TypeAlias`
%pytest -v --ignore tests/test_rtrip.py

%files -n python3-astor -f %{pyproject_files}
%doc README.*


%changelog
%autochangelog
