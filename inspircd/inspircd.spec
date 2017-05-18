Name:           inspircd
Version:        2.0.24
Release:        1%{?dist}
Summary:        InspIRCd is a modular Internet Relay Chat (IRC) server

License:        GPLv2
URL:            http://inspircd.org

Source0:        https://github.com/inspircd/inspircd/archive/v%{version}.tar.gz
Source1:        inspircd.service
Source2:        inspircd.conf
Source3:        links.conf
Source4:        opers.conf
Source5:        modules.conf

Requires: gnutls
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd,gnutls-devel


%description
InspIRCd is a modular Internet Relay Chat (IRC) server written in C++ for Linux,
BSD, Windows and Mac OS X systems which was created from scratch to be stable,
modern and lightweight.


%pre
getent group ircd >/dev/null || groupadd -r ircd
getent passwd ircd >/dev/null || \
    useradd -r -g ircd -d /dev/null -s /sbin/nologin \
    -c "IRCD User" ircd
exit 0


%post
%systemd_post inspircd.service


%preun
%systemd_preun inspircd.service
systemctl reset-failed


%postun
%systemd_postun inspircd.service



%prep
%setup -q

%build
%configure --system
%configure --enable-extras=m_ssl_gnutls.cpp
make %{?_smp_mflags}


%install
%make_install
mkdir $RPM_BUILD_ROOT/usr/bin
mv $RPM_BUILD_ROOT/usr/inspircd $RPM_BUILD_ROOT/usr/bin/inspircd
mkdir -p $RPM_BUILD_ROOT/var/log/inspircd
mkdir -p $RPM_BUILD_ROOT/var/inspircd

mkdir -p $RPM_BUILD_ROOT%{_unitdir}/
install %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/

install %{SOURCE2} $RPM_BUILD_ROOT/etc/inspircd/
install %{SOURCE3} $RPM_BUILD_ROOT/etc/inspircd/
install %{SOURCE4} $RPM_BUILD_ROOT/etc/inspircd/
install %{SOURCE5} $RPM_BUILD_ROOT/etc/inspircd/


%files
%doc
/usr/lib/inspircd/*.so
/usr/sbin/inspircd
/etc/inspircd/examples
/usr/bin/inspircd
%dir %attr(755, ircd, ircd) /var/log/inspircd
%dir %attr(755, ircd, ircd) /var/inspircd
%config /etc/inspircd/*.conf
%{_unitdir}/inspircd.service
%define _unpackaged_files_terminate_build 0


%changelog
