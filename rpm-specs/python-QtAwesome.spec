%global pypi_name QtAwesome
%global simple_name qtawesome

Name:       python-%{pypi_name}
Version:    1.3.1
Release:    %autorelease

Summary:    FontAwesome icons in PyQt and PySide applications
# MIT: QtAwesome code and the bundled phosphor and remixicon fonts
# CC-BY-4.0: the bundled codicon font
# Apache-2.0: the bundled material design icons fonts
# OFL-1.1: the bundled elusive icons font
# OFL-1.1-RFN: the bundled fontawesome icon fonts
%if 0%{?fedora} > 38
License:    MIT AND CC-BY-4.0 AND Apache-2.0 AND OFL-1.1
%else
License:    MIT AND CC-BY-4.0 AND Apache-2.0 AND OFL-1.1 AND OFL-1.1-RFN
%endif
URL:        https://github.com/spyder-ide/%{simple_name}

Source0:    %pypi_source

BuildArch:  noarch

BuildRequires:  python3-devel

%description
QtAwesome enables iconic fonts such as Font Awesome and Elusive.

It is a port to Python - PyQt / PySide of the QtAwesome C++ library by 
Rick Blommers.

%package -n     python3-%{pypi_name}
Summary:    FontAwesome icons in PyQt and PySide applications
%{?python_provide:%python_provide python3-%{pypi_name}}

#provides font files
#./qtawesome/fonts/codicon.ttf
Provides:   bundled(codicon-fonts) = 1.10
#./qtawesome/fonts/elusiveicons-webfont.ttf
Provides:   bundled(elusiveicons-fonts) = 001.000
#./qtawesome/fonts/materialdesignicons5-webfont.ttf
Provides:   bundled(materialdesignicons5-fonts) = 5.9.55
#./qtawesome/fonts/materialdesignicons6-webfont.ttf
Provides:   bundled(materialdesignicons6-fonts) = 1.0
#./qtawesome/fonts/phosphor.ttf
Provides:   bundled(phosphor-fonts) = 1.3
#./qtawesome/fonts/remixicon.ttf
Provides:   bundled(remixicon-fonts) = 2.5
%if 0%{?fedora} > 38
Requires:   fontawesome4-fonts-web
Requires:   fontawesome-fonts-web
%else
#./qtawesome/fonts/fontawesome4-webfont-4.7.ttf
Provides:   bundled(fontawesome-fonts-web) = 4.7.0
#./qtawesome/fonts/fontawesome5-brands-webfont-5.15.4.ttf
#./qtawesome/fonts/fontawesome5-regular-webfont-5.15.4.ttf
#./qtawesome/fonts/fontawesome5-solid-webfont-5.15.4.ttf
Provides:   bundled(fontawesome5-fonts-web) = 5.15.4
%endif

%description -n python3-%{pypi_name}

QtAwesome enables iconic fonts such as Font Awesome and Elusive.

It is a port to Python - PyQt / PySide of the QtAwesome C++ library by 
Rick Blommers.

%prep
%autosetup -n %{pypi_name}-%{version}

# Fix end of line encoding
sed -i 's/\r//' README.md

# Don't use the bundled fonts.
# This disables verifying the checksum of font files.
%if 0%{?fedora} > 38
sed -i '/^SYSTEM_FONTS = /s/False/True/' qtawesome/iconic_font.py
%endif

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l qtawesome

%if 0%{?fedora} > 38
# Unbundle the fontawesome 4.x font
rm %{buildroot}%{python3_sitelib}/qtawesome/fonts/fontawesome4-webfont-4.7.ttf
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.ttf \
      %{buildroot}%{python3_sitelib}/qtawesome/fonts/fontawesome4-webfont-4.7.ttf
# Unbundle the fontawesome 5.x fonts
# Version 6 is backwards compatible with version 5
rm %{buildroot}%{python3_sitelib}/qtawesome/fonts/fontawesome5-*.ttf
ln -s %{_datadir}/fontawesome/webfonts/fa-brands-400.ttf \
      %{buildroot}%{python3_sitelib}/qtawesome/fonts/fontawesome5-brands-webfont-5.15.4.ttf
ln -s %{_datadir}/fontawesome/webfonts/fa-regular-400.ttf \
      %{buildroot}%{python3_sitelib}/qtawesome/fonts/fontawesome5-regular-webfont-5.15.4.ttf
ln -s %{_datadir}/fontawesome/webfonts/fa-solid-900.ttf \
      %{buildroot}%{python3_sitelib}/qtawesome/fonts/fontawesome5-solid-webfont-5.15.4.ttf
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%{_bindir}/qta-browser

%changelog
%autochangelog
