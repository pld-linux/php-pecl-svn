%define		_modname	svn
%define		_status		beta
Summary:	PHP Bindings for the Subversion Revision control system
Summary(pl.UTF-8):	Dowiązania PHP do systemou kontroli rewizji Subversion
Name:		php-pecl-%{_modname}
Version:	0.4.1
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	79b1328090e8241500f51a0a211ce5fd
URL:		http://pecl.php.net/package/svn/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	re2c >= 0.12.0
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	subversion-devel < 1.5
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bindings for the Subversion revision control system, providing a
method for manipulating a working copy or repository with PHP.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Pakiet ten dostarcza dowiązań do systemu kontroli rewizji Subversion,
dostarczając metod do obróbki lokalną kopią lub repozytorium z poziomu
PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make} \
	CFLAGS="%{rpmcflags} $(apu-1-config --includes)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
