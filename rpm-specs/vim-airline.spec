%global forgeurl https://github.com/%{name}/%{name}
# Switch to latest master branch, see:
# https://github.com/vim-airline/vim-airline/issues/2445
%global commit ff0f9a45a5d81d2c8aa67601c264b18c4fe26b15

Name:           vim-airline
Version:        0.11
%forgemeta
Release:        %autorelease
Summary:        Lean & mean status/tabline for vim that's light as air

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        %{name}.metainfo.xml
BuildArch:      noarch

BuildRequires:  libappstream-glib
BuildRequires:  vim-filesystem
Requires:       vim-enhanced

%description
%{summary}.

When the plugin is correctly loaded, Vim will draw a nice statusline at the
bottom of each window.


%prep
%forgeautosetup -p1


%install
mkdir -p                        %{buildroot}%{vimfiles_root}
cp -r {autoload,plugin}         %{buildroot}%{vimfiles_root}
install -m 0644 -Dp %{SOURCE1}  %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml


%files
%license LICENSE
%doc README.md CHANGELOG.md CONTRIBUTING.md doc/*
%{vimfiles_root}/autoload/*
%{vimfiles_root}/plugin/*
%{_metainfodir}/*.xml


%changelog
%autochangelog
