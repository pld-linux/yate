# TODO:
# - subpackages for qt client (and maybe gtk)

Summary:	Yet Another Telephony Engine
Summary(pl):	Yet Another Telephony Engine - jeszcze jeden silnik do telefonii
Name:		yate
Version:	0.8.7
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://yate.null.ro/tarballs/%{name}-%{version}.tar.gz
# Source0-md5:	96e2e915a3485fe5f4621c80586569d4
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://yate.null.ro/
BuildRequires:	glib2-devel
BuildRequires:	libgsm-devel
BuildRequires:	libpri-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openh323-devel
BuildRequires:	ortp-devel
BuildRequires:	postgresql-devel
BuildRequires:	pwlib-devel
BuildRequires:	qt-devel
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkonfig
Requires(post):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
YATE is a telephony engine designed to implement PBX and IVR solutions
for small to large scale projects.

%description -l pl
YATE to silnik do telefonii zaprojektowany do implementacji rozwi±zañ
opartych na PBX oraz IVR zarówno w du¿ych jak i ma³ych projektach.

%package devel
Summary:	Header files for YATE libraries
Summary(pl):	Pliki nag³ówkowe bibliotek YATE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the header files for YATE libraries.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe bibliotek YATE.

%prep
%setup -q -n %{name}
sed -i -e 's#/usr/include/qt3#%{_includedir}/qt#g' configure*

%build
%configure \
	--enable-shared \
	--enable-static \
	--with-libpq \
	--with-libpri \
	--with-libgsm \
	--with-pwlib \
	--with-openh323 \
	--with-libortp \
	--with-libglib2 \
	--without-libgtk \
	--with-libqt=%{_prefix}
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
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/%{name} start\" to start %{name} server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop >&2
        fi
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
