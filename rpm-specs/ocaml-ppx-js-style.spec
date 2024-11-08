# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

Name:           ocaml-ppx-js-style
Version:        0.17.0
Release:        %autorelease
Summary:        Code style checker for Jane Street OCaml packages

License:        MIT
URL:            https://github.com/janestreet/ppx_js_style
VCS:            git:%{url}.git
Source:         %{url}/archive/v%{version}/ppx_js_style-%{version}.tar.gz

BuildRequires:  ocaml >= 5.1.0
BuildRequires:  ocaml-base-devel >= 0.17
BuildRequires:  ocaml-dune >= 3.11.0
BuildRequires:  ocaml-octavius-devel
BuildRequires:  ocaml-ppxlib-devel >= 0.28.0

%description
Ppx_js_style is an identity ppx rewriter that enforces Jane Street
coding styles.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-base-devel%{?_isa}
Requires:       ocaml-octavius-devel%{?_isa}
Requires:       ocaml-ppxlib-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n ppx_js_style-%{version}

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
%autochangelog
