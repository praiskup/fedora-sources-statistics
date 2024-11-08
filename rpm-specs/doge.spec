Name:           doge
Version:        3.6.0
Release:        %autorelease
Summary:        MOTD script based on the doge meme

License:        MIT
URL:            https://github.com/thiderman/doge
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
doge is a simple motd script based on the doge meme. It prints random
grammatically incorrect statements that are sometimes based on things from your
computer.


%prep
%autosetup
# such shebangs wow
sed -i -e '/^#!\//, 1d' doge/*.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files doge

 
%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
%autochangelog
