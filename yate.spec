# TODO:
# - subpackages for qt client (and maybe gtk)
Summary:	Yet Another Telephony Engine
Summary(pl.UTF-8):	Yet Another Telephony Engine - jeszcze jeden silnik do telefonii
Name:		yate
Version:	3.0.0
Release:	0.3.1
License:	GPL
Group:		Applications/Communications
Source0:	http://voip.null.ro/tarballs/yate3/%{name}-%{version}-alpha3.tar.gz
# Source0-md5:	3e900669f5aad67c2dbc0ca2cd5cc7b0
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://yate.null.ro/
BuildRequires:	glib2-devel
BuildRequires:	libgsm-devel
BuildRequires:	libpri-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openh323-devel
#BuildRequires:	ortp-devel
BuildRequires:	postgresql-devel
BuildRequires:	pwlib-devel
#BuildRequires:	qt-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkonfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
YATE is a telephony engine designed to implement PBX and IVR solutions
for small to large scale projects.

%description -l pl.UTF-8
YATE to silnik do telefonii zaprojektowany do implementacji rozwiązań
opartych na PBX oraz IVR zarówno w dużych jak i małych projektach.

%package devel
Summary:	Header files for YATE libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek YATE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the header files for YATE libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe bibliotek YATE.

%prep
%setup -q -n %{name}
sed -i -e 's#/usr/include/qt3#%{_includedir}/qt#g' configure*

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-libpq \
	--with-libgsm \
	--with-pwlib \
	--with-openh323
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
touch $RPM_BUILD_ROOT/var/log/yate.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(750,root,root) %dir %{_sysconfdir}/yate
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/yate/*
%attr(755,root,root) %{_libdir}/lib*.so.*
%attr(755,root,root) %{_bindir}/yate
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root)  %{_libdir}/%{name}/*.%{name}
%{_mandir}/man?/yate.*
%{_libdir}/%{name}/*.php
%{_libdir}/%{name}/*.pm
%ghost /var/log/yate.log
%exclude %{_libdir}/%{name}/*qt*.%{name}

%files devel
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_bindir}/yate-config
%{_includedir}/*
%{_mandir}/man?/yate-config.*
%{_pkgconfigdir}/*.pc
