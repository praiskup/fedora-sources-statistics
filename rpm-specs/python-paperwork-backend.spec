%global srcname paperwork-backend
%global srcname_ paperwork_backend

Name:           python-%{srcname}
Version:        2.2.5
Release:        %autorelease
Summary:        Paperwork's backend

License:        GPL-3.0-or-later
URL:            https://gitlab.gnome.org/World/OpenPaperwork/paperwork/tree/master/paperwork-backend
Source0:        %pypi_source %{srcname_}
# https://gitlab.gnome.org/World/OpenPaperwork/paperwork/-/issues/1035
Patch0001:      0001-Skip-docx-duplicated-import-test-entirely.patch

BuildArch:      noarch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

BuildRequires:  python3-devel

%global _description %{expand: \
Paperwork is a tool to make papers searchable. The basic idea behind Paperwork
is "scan & forget" : You should be able to just scan a new document and forget
about it until the day you need it.

This is the backend part of Paperwork. It manages:
    The work directory / Access to the documents;
    Indexing;
    Searching;
    Suggestions;
    Import;
    Export.
}

%description %{_description}


%package -n     python3-%{srcname}
Summary:        %{summary}

BuildRequires:  python3dist(openpaperwork-gtk)
BuildRequires:  python3dist(pycairo)

BuildRequires:  python3-gobject
BuildRequires:  libinsane-gobject
BuildRequires:  libreoffice
BuildRequires:  poppler-glib
BuildRequires:  sane-backends-drivers-scanners
BuildRequires:  tesseract
BuildRequires:  tesseract-osd

Requires:       libinsane-gobject
Recommends:     libreoffice
Requires:       python3dist(pygobject)
Requires:       python3dist(pycairo)
Requires:       poppler-glib
Requires:       tesseract
Requires:       tesseract-osd

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname_}-%{version} -p2

find tests -name '*.pyc' -delete

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname_}

%check
PATH=%{buildroot}%{_bindir}:$PATH PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{python3} -m unittest discover --verbose -s tests

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.markdown
%license LICENSE

%changelog
%autochangelog
