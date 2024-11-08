%global srcname timeslot
%global commit af35445e96cbb2f3fb671a75aac6aa93e4e7e7a6
%global short_commit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{srcname}
Version:        0.1.2^20240509.%{short_commit}
Release:        %autorelease
Summary:        Class for working with time slots that have an arbitrary start and end

License:        MIT
URL:            https://github.com/ErikBjare/%{srcname}
Source:         %{url}/archive/%{commit}/%{srcname}-%{short_commit}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Completes the Python datetime module: datetime (a time), time delta
(a duration), timezone (an offset), timeslot (a range/interval).

Supports operations such as: overlaps, intersects, contains, intersection,
adjacent, gap, union.

Initially developed as part of aw-core, and inspired by a similar library for
.NET.

You might also be interested in pandas.Interval.}

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{commit}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -ri '/^[[:blank:]]*pytest-cov\b/d' pyproject.toml
sed -ri '/--cov=timeslot/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
%autochangelog
