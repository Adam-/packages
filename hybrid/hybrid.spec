Name:           ircd-hybrid
Version:        8.2.12
Release:        1%{?dist}
Summary:        A lightweight, high-performance internet relay chat daemon.

License:        GPL
URL:            http://www.ircd-hybrid.org

Source0:        https://github.com/ircd-hybrid/ircd-hybrid/archive/%{version}.tar.gz
Source1:        hybrid.service
Source2:        ircd.conf

#Requires: gnutls
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd byacc flex


%description
ircd-hybrid is a lightweight, high-performance internet relay chat daemon.


%pre
getent group ircd >/dev/null || groupadd -r ircd
getent passwd ircd >/dev/null || \
    useradd -r -g ircd -d /dev/null -s /sbin/nologin \
    -c "IRCD User" ircd
exit 0


%post
%systemd_post hybrid.service


%preun
%systemd_preun hybrid.service
systemctl reset-failed


%postun
%systemd_postun hybrid.service



%prep
%setup -q

%build
#%configure --disable-openssl --enable-gnutls
%configure --disable-openssl --localstatedir=/var/ircd
make %{?_smp_mflags}


%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_unitdir}/
install %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/

install %{SOURCE2} $RPM_BUILD_ROOT/etc/


%files
%doc
/usr/bin/ircd
/usr/bin/mkpasswd
/usr/lib64/ircd-hybrid/
/usr/share/ircd-hybrid/
/usr/share/man/man8/ircd.8.gz
%attr(-, ircd, ircd) /var/ircd/lib
%attr(-, ircd, ircd) /var/ircd/log
%attr(-, ircd, ircd) /var/ircd/run
%config /etc/ircd.conf
%{_unitdir}/hybrid.service
%define _unpackaged_files_terminate_build 0


%changelog
* Wed Jan 27 2016 Adam <Adam@anope.org>
- Initial release

- 
