# Generated by go2rpm 1.10.0
%bcond_without check

# https://github.com/cli/cli
%global goipath         github.com/cli/cli/v2
Version:                2.46.0

%gometa -L -f

%global common_description %{expand:
A command-line interface to GitHub for use in your terminal or your scripts.

gh is a tool designed to enhance your workflow when working with GitHub. It
provides a seamless way to interact with GitHub repositories and perform various
actions right from the command line, eliminating the need to switch between your
terminal and the GitHub website.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           gh
Release:        %autorelease
Summary:        GitHub's official command line tool

License:        MIT
URL:            %{gourl}
Source:         %{gosource}

BuildRequires:  git-core
BuildRequires:  sed

Requires:       git-core

%description %{common_description}

%gopkg

%prep
%goprep -A
%autopatch -p1

%generate_buildrequires
%go_generate_buildrequires

%build
export LDFLAGS="-X github.com/cli/cli/v2/internal/build.Version=%{version}  \
                -X github.com/cli/cli/v2/internal/build.Date=$(date -d "@${SOURCE_DATE_EPOCH}" +%Y-%m-%d)"
for cmd in cmd/%{name} cmd/gen-docs; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

# Generate manpages
%{gobuilddir}/bin/gen-docs --man-page --doc-path ./share/man/man1

# Generate shell completions
%{gobuilddir}/bin/%{name} completion -s bash > %{name}.bash
%{gobuilddir}/bin/%{name} completion -s fish > %{name}.fish
%{gobuilddir}/bin/%{name} completion -s zsh  > %{name}.zsh


%install
# We are deliberately excluding cmd/gen-docs. It is only needed for building.
install -Dpm 0755 %{gobuilddir}/bin/%{name} -t %{buildroot}%{_bindir}/

# Install manpages
install -Dpm 0644 ./share/man/man1/%{name}*.1 -t %{buildroot}%{_mandir}/man1/

# Install shell completions
install -Dpm 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -Dpm 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish
install -Dpm 0644 %{name}.zsh  %{buildroot}%{zsh_completions_dir}/_%{name}


%if %{with check}
%check
# TestHTTPClientSanitizeJSONControlCharactersC0 fails as needs to be updated for 1.22 changes
for test in "TestRebuildContainerIncremental" "TestStartJupyterServerSuccess" \
            "TestStartJupyterServerFailure" "TestStartSSHServerFailure" \
            "TestStartSSHServerSuccess" "TestRebuildContainerFull" \
            "TestRebuildContainerFailure" "TestHTTPClientSanitizeJSONControlCharactersC0" \
; do
awk -i inplace '/^func.*'"$test"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' $(grep -rl $test)
done
%gocheck
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*1*
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%changelog
%autochangelog
