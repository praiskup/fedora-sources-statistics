%global pypi_name pyftpdlib

Name:           python-%{pypi_name}
Version:        2.0.0
Release:        %autorelease
Summary:        Very fast asynchronous FTP server library

%global distprefix %{nil}
%global forgeurl https://github.com/giampaolo/pyftpdlib
%global tag release-%{version}
%forgemeta

License:        MIT
URL:            %forgeurl
Source:         %forgesource

BuildArch:      noarch

BuildRequires:  help2man
BuildRequires:  python3-devel
BuildRequires:  python3dist(psutil)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-xdist)


%global desc %{expand: \
Python FTP server library provides a high-level portable interface to
easily write very efficient, scalable and asynchronous FTP servers with
Python. It is the most complete RFC-959 FTP server implementation
available for Python programming language.

** Features **

- Extremely lightweight, fast and scalable
- Uses sendfile(2) system call for uploads
- Uses epoll() / kqueue() / select() to handle concurrency asynchronously
- Can optionally skip to a multiple thread / process model (as in:
  you’ll be free to block or use slow filesystems)
- Portable: entirely written in pure Python; works with Python 2.7 and
  3.x using a single code base
- Supports FTPS (RFC-4217), IPv6 (RFC-2428),
  Unicode file names (RFC-2640), MLSD/MLST commands (RFC-3659)
- Support for virtual users and virtual filesystem
- Flexible system of "authorizers" able to manage both "virtual" and
  "real" users on both UNIX and Windows

** Performance **

Despite being written in an interpreted language, pyftpdlib has
transfer rates comparable or superior to common UNIX FTP servers
written in C. It usually tends to scale better because whereas vsftpd
and proftpd use multiple processes to achieve concurrency, pyftpdlib
only uses one.}

%description 
%{desc}


%package -n python3-%{pypi_name}
Summary:        %{summary}
Provides:       ftpbench = %{?epoch:%{epoch}:}%{version}-%{release}
# Package falls back to not supporting SSL if not installed
Recommends:     python3dist(pyftpdlib[ssl])
# Optional dependency for `ftpbench`
Suggests:       python3dist(psutil)

%description -n python3-%{pypi_name} %{desc}


%pyproject_extras_subpkg -n python3-%{pypi_name} ssl


%prep
%forgeautosetup -p1

# do not install tests
sed -i "s/, 'pyftpdlib.test'//" setup.py

# `psutil` >= 6 has renamed `connections` to `net_connections`. However,
# current version in Fedora is 5.9.8.
sed -r \
    -e 's/(this_proc\.)net_(connections)/\1\2/' \
    -i pyftpdlib/test/__init__.py


%generate_buildrequires
%pyproject_buildrequires -x ssl


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}


mkdir -p %{buildroot}%{_mandir}/man1
%{py3_test_envvars} \
  help2man --no-info --version-string 'ftpbench %{version}' \
  -o %{buildroot}%{_mandir}/man1/ftpbench.1 --no-discard-stderr \
  %{buildroot}%{_bindir}/ftpbench


%check
# Tests fail in Koji, but not in Copr or with mock
k="${k-}${k+ and }not test_mlst"
k="${k-}${k+ and }not test_nlst"

%pytest -v -n auto --dist loadgroup \
        ${k+-k }"${k-}"


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc HISTORY.rst README.rst
%{_bindir}/ftpbench
%{_mandir}/man1/ftpbench.1*


%changelog
%autochangelog
