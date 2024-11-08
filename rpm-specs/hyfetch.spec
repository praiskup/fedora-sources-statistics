Name:           hyfetch
Version:        1.99.0
Release:        %autorelease
Summary:        Customizable Linux System Information Tool

License:        MIT
URL:            https://github.com/hykilpikonna/HyFetch
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description
HyFetch is a command line tool to display information about your
Linux system, such as amount of installed packages, OS and kernel
version, active GTK theme, CPU info, and used/available memory.
It is a fork of neofetch, and adds pride flag coloration to the OS logo.

%prep
%autosetup -p1 -n %{name}-%{version}

# remove tools/ directory to conform to its pypi source
rm -rf tools/

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l hyfetch

install -pDm 644 hyfetch/scripts/autocomplete.bash %{buildroot}%{bash_completions_dir}/hyfetch
install -pDm 644 hyfetch/scripts/autocomplete.zsh %{buildroot}%{zsh_completions_dir}/_hyfetch

%check
%pyproject_check_import

%files -n hyfetch -f %{pyproject_files}
%{_bindir}/hyfetch
%{_bindir}/neowofetch
%{bash_completions_dir}/hyfetch
%{zsh_completions_dir}/_hyfetch

%changelog
%autochangelog
