# TODO:
# - subpackages for qt client (and maybe gtk)

Summary:	Yet Another Telephony Engine
Name:		yate
Version:	0.8.7
Release:	1
License:	GPL
Source0:	http://yate.null.ro/%{name}-%{version}.tar.gz
# Source0-md5:	96e2e915a3485fe5f4621c80586569d4
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Group:		Applications/Communications
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
URL:		http://yate.null.ro/
BuildRequires:	libstdc++
BuildRequires:	pwlib-devel
BuildRequires:	qt-devel
BuildRequires:	libgsm-devel
BuildRequires:	openh323-devel
BuildRequires:	glib2-devel
BuildRequires:	libpri-devel
BuildRequires:	postgresql-devel
BuildRequires:	ortp-devel
BuildRequires:	spandsp-devel

%description
YATE is a telephony engine designed to implement PBX and IVR solutions
for small to large scale projects.

%package devel
Summary:	Development package for yate
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The yate-devel package includes the libraries and header files for
YATE

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
install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig},var/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
touch $RPM_BUILD_ROOT/var/log/yate.log

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(750,root,root) %dir %{_sysconfdir}/yate
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/yate/*
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
