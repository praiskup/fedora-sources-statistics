# This specfile is licensed under:
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Fedora Project Authors
# SPDX-FileCopyrightText: 2022 Maxwell G <gotmax@e.email>
# See %%{name}.spec.license for the full license text.

%bcond_without tests

Name:           yt-dlp
Version:        2024.10.22
Release:        1%{?dist}
Summary:        A command-line program to download videos from online video platforms

License:        Unlicense
URL:            https://github.com/%{name}/%{name}
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# License of the specfile
Source:         yt-dlp.spec.license

# https://github.com/yt-dlp/yt-dlp/commit/6f9e6537434562d513d0c9b68ced8a61ade94a64
# [rh:websockets] Upgrade websockets to 13.0 (#10815)
# Revert this patch for compatibility with older Fedora versions
Patch1000:      websockets-13.patch

BuildArch:      noarch

BuildRequires:  python3-devel

# Needed for %%prep
BuildRequires:  tomcli

%if %{with tests}
# Needed for %%check
BuildRequires:  %{py3_dist pytest}
%endif

# Needed for docs
BuildRequires:  pandoc
BuildRequires:  make

# ffmpeg-free is now available in Fedora.
Recommends:     /usr/bin/ffmpeg
Recommends:     /usr/bin/ffprobe

Suggests:       python3dist(keyring)

%global _description %{expand:
yt-dlp is a command-line program to download videos from many different online
video platforms, such as youtube.com. The project is a fork of youtube-dl with
additional features and fixes.}

%description %{_description}

%package bash-completion
Summary:        Bash completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)

%description bash-completion
Bash command line completion support for %{name}.

%package zsh-completion
Summary:        Zsh completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)

%description zsh-completion
Zsh command line completion support for %{name}.

%package fish-completion
Summary:        Fish completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} and fish)

%description fish-completion
Fish command line completion support for %{name}.

%prep
%autosetup -N
%if %{defined fedora} && %{fedora} <= 41
# Revert patch for compatibility with older websockets
%patch -P1000 -p1 -R
%endif

# Remove unnecessary shebangs
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
# Relax version constraints
tomcli-set pyproject.toml lists replace project.dependencies \
    '(requests|urllib3|websockets)>=.*' '\1'

%generate_buildrequires
%pyproject_buildrequires -r

%build
# Docs and shell completions
make yt-dlp.1 completion-bash completion-zsh completion-fish

# Docs and shell completions are also included in the wheel.
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files yt_dlp

%check
%if %{with tests}
# See https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/run_tests.sh
%pytest -k "not download"
%endif

%files -f %{pyproject_files}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%doc README.md
%license LICENSE

%files bash-completion
%{bash_completions_dir}/%{name}

%files zsh-completion
%{zsh_completions_dir}/_%{name}

%files fish-completion
%{fish_completions_dir}/%{name}.fish

%changelog
* Wed Oct 23 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.10.22-1
- Update to 2024.10.22. Fixes rhbz#2321221

* Tue Oct 08 2024 Maxwell G <maxwell@gtmx.me> - 2024.10.07-1
- Update to 2024.10.07.

* Sat Sep 28 2024 Maxwell G <maxwell@gtmx.me> - 2024.09.27-1
- Update to 2024.09.27.

* Mon Aug 12 2024 Maxwell G <maxwell@gtmx.me> - 2024.08.06-1
- Update to 2024.08.06. Fixes rhbz#2303069.

* Sat Aug 03 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.08.01-1
- Update to 2024.08.01. Fixes rhbz#2302522

* Fri Jul 26 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.07.25-1
- Update to 2024.07.25. Fixes rhbz#2300087

* Wed Jul 24 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.07.16-1
- Update to 2024.07.16. Fixes rhbz#2298550

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.07.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.07.09-1
- Update to 2024.07.09. Fixes rhbz#2297344

* Mon Jul 08 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.07.07-1
- Update to 2024.07.07. Fixes rhbz#2296356

* Thu Jul 04 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.07.02-1
- Update to 2024.07.02. Fixes rhbz#2295769

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2024.05.27-2
- Rebuilt for Python 3.13

* Wed May 29 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.05.27-1
- Update to 2024.05.27. Fixes rhbz#2283578.

* Mon May 27 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2024.05.26-1
- Update to 2024.05.26. Fixes rhbz#2274266.

* Wed Apr 10 2024 Maxwell G <maxwell@gtmx.me> - 2024.04.09-1
- Update to 2024.04.09.

* Wed Mar 13 2024 Maxwell G <maxwell@gtmx.me> - 2024.03.10-1
- Update to 2024.03.10. Fixes rhbz#2268944.

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.12.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 3 2024 Maxwell G <maxwell@gtmx.me> - 2023.12.30-1
- Update to 2023.12.30. Fixes rhbz#2244200.

* Wed Oct 11 2023 Marcus Müller <marcus_fedora@baseband.digital> - 2023.10.07-1
- Update to 2023.10.07.
- Fixes rhbz#2243274
- Fixes rhbz#2240465

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.07.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Maxwell G <maxwell@gtmx.me> - 2023.07.06-1
- Update to 2023.07.06.
- Mitigates CVE-2023-35934 / GHSA-v8mc-9377-rwjj

* Wed Jul 05 2023 Maxwell G <maxwell@gtmx.me> - 2023.06.22-1
- Update to 2023.06.22. Fixes rhbz#2216612.

* Thu Jun 22 2023 Maxwell G <maxwell@gtmx.me> - 2023.06.21-1
- Update to 2023.06.21. Fixes rhbz#2216612.

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2023.03.04-2
- Rebuilt for Python 3.12

* Mon Mar 06 2023 Maxwell G <maxwell@gtmx.me> - 2023.03.04-1
- Update to 2023.03.04. Fixes rhbz#2175395.

* Fri Feb 17 2023 Maxwell G <maxwell@gtmx.me> - 2023.02.17-1
- Update to 2023.02.17.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.01.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Maxwell G <gotmax@e.email> - 2023.01.06-1
- Update to 2023.01.06. Fixes rhbz#2157879.

* Mon Nov 14 2022 Maxwell G <gotmax@e.email> - 2022.11.11-1
- Update to 2022.11.11. Fixes rhbz#2142417.

* Sat Oct 08 2022 Maxwell G <gotmax@e.email> - 2022.10.04-1
- Update to 2022.10.04. Fixes rhbz#2132726.

* Fri Sep 02 2022 Maxwell G <gotmax@e.email> - 2022.09.01-1
- Update to 2022.09.01. Fixes rhbz#2123442.

* Fri Aug 19 2022 Maxwell G <gotmax@e.email> - 2022.08.19-1
- Update to 2022.08.19. Fixes rhbz#2118224.

* Tue Aug 09 2022 Maxwell G <gotmax@e.email> - 2022.08.08-1
- Update to 2022.08.08.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.06.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 04 2022 Maxwell G <gotmax@e.email> - 2022.06.29-2
- Fix shell completions subpackages

* Mon Jul 04 2022 Maxwell G <gotmax@e.email> - 2022.06.29-1
- Update to 2022.06.29. Fixes rhbz#2102238.

* Thu Jun 23 2022 Maxwell G <gotmax@e.email> - 2022.06.22.1-1
- Update to 2022.06.22.1. Fixes rhbz#2100019.

* Fri Jun 17 2022 Maxwell G <gotmax@e.email> - 2022.05.18-3
- Fix gating configuration

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2022.05.18-2
- Rebuilt for Python 3.11

* Tue May 24 2022 Maxwell G <gotmax@e.email> - 2022.05.18-1
- Update to 2022.05.18. Fixes rhbz#2088564.

* Fri Apr 08 2022 Maxwell G <gotmax@e.email> - 2022.04.08-1
- Update to 2022.04.08. Fixes rhbz#2073359.

* Sat Mar 12 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 2022.03.08.1-2
- build: Make ffmpeg and ffprobe conditional deps for >= f36 only

* Thu Mar 10 2022 Maxwell G <gotmax@e.email> - 2022.03.08.1-1
- Update to 2022.03.08.1. Fixes rhbz#2061973.

* Mon Mar 07 2022 Maxwell G <gotmax@e.email> - 2022.02.04-2
- Add weak dependency on ffmpeg and ffprobe.
- Make shell-completion subpackages optional again.

* Fri Feb 04 2022 Maxwell G <gotmax@e.email> - 2022.2.4-1
- Update to 2022.2.4. Fixes rhbz#2050497.

* Mon Jan 24 2022 Maxwell G <gotmax@e.email> - 2022.01.21-1
- Update to 2022.01.21.

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.12.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Maxwell G <gotmax@e.email> - 2021.12.27-1
- Update to 2021.12.27.

* Sun Dec 26 2021 Maxwell G <gotmax@e.email> - 2021.12.25-1
- Update to 2021.12.25.

* Wed Dec 01 2021 Maxwell G <gotmax@e.email> - 2021.12.01-1
- Update to 2021.12.01.

* Tue Nov 9 2021 Maxwell G <gotmax@e.email> - 2021.11.10.1-1
- Update to 2021.11.10.1.

* Tue Nov 9 2021 Maxwell G <gotmax@e.email> - 2021.10.22-2
- Skip installing unnecessary tox dependencies
- Fix shell-completion subpackages
- Only package README.md; don't generate extra README.txt

* Sat Oct 23 2021 Maxwell G <gotmax@e.email> - 2021.10.22-1
- Update to 2021.10.22

* Sun Oct 10 2021 Maxwell G <gotmax@e.email> - 2021.10.10-1
- Mark LICENSE with %%license instead of %%doc
- Update to 2021.10.10
- Fix non-executable-script rpmlint error
- Use `python3dist(NAME)` for dependencies
- Fix rpm-buildroot-usage rpmlint error

* Sat Oct 9 2021 Maxwell G <gotmax@e.email> - 2021.10.09-1
- Initial package
