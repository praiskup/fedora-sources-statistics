# Generated by go2rpm 1.14.0
%bcond check 1

# https://github.com/gopasspw/gopass-jsonapi
%global goipath         github.com/gopasspw/gopass-jsonapi
Version:                1.15.14

%gometa -L -f

%global common_description %{expand:
Gopass Browser Bindings.}

Name:           gopass-jsonapi
Release:        %autorelease
Summary:        Gopass Browser Bindings

# Generated by go-vendor-tools
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSD-3-Clause-HP AND ISC AND MIT AND MPL-2.0 AND (Apache-2.0 OR MIT)
URL:            %{gourl}
Source0:        %{gosource}
# Generated by go-vendor-tools
Source1:        %{archivename}-vendor.tar.bz2
Source2:        go-vendor-tools.toml

BuildRequires:  go-vendor-tools
BuildRequires:  git-core
BuildRequires:  gnupg2

%description %{common_description}

%prep
%goprep -A
%setup -q -T -D -a1 %{forgesetupargs}
%autopatch -p1

%generate_buildrequires
%go_vendor_license_buildrequires -c %{S:2}

%build
%gobuild -o %{gobuilddir}/bin/gopass-jsonapi %{goipath}

%install
%go_vendor_license_install -c %{S:2}
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%go_vendor_license_check -c %{S:2}
%if %{with check}
%gocheck
%endif

%files -f %{go_vendor_license_filelist}
%license vendor/modules.txt
%doc docs CHANGELOG.md README.md
%{_bindir}/gopass-jsonapi


%changelog
%autochangelog