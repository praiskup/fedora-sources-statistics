Name:           opensuse-distro-aliases
Version:        0.2.0
Release:        %autorelease
Summary:        Aliases for active openSUSE releases

License:        MIT
URL:            https://github.com/rpm-software-management/opensuse-distro-aliases
Source:         %{pypi_source opensuse_distro_aliases}
BuildArch:      noarch

BuildRequires:  python3-devel

%generate_buildrequires
%pyproject_buildrequires


%global _description %{expand:
This project provides a list of the currently
maintained openSUSE distributions. It is the openSUSE equivalent of
fedora-distro-aliases.}

%description %_description

%package -n     python3-opensuse-distro-aliases
Summary:        %{summary}

%description -n python3-opensuse-distro-aliases %_description


%prep
%autosetup -p1 -n opensuse_distro_aliases-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files opensuse_distro_aliases


%check
%pyproject_check_import -t


%files -n python3-opensuse-distro-aliases -f %{pyproject_files}
%license COPYING
%doc README.rst


%changelog
%autochangelog
