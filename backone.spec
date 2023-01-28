Name:           backone
Version:        1.6.6
Release:        1%{?dist}
Summary:        BackOne global ethernet switch

License:        BackOne BSL 1.1
URL:            https://backone.cloud

%if 0%{?rhel} >= 7
BuildRequires:  systemd
%endif

%if 0%{?fedora} >= 21
BuildRequires:  systemd
%endif

Requires:       iproute libstdc++

%if 0%{?rhel} >= 7
Requires:       systemd
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%if 0%{?rhel} <= 6
Requires:       chkconfig
%endif

%if 0%{?fedora} >= 21
Requires:       systemd
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%description
BackOne is a software defined networking layer for Earth.

It can be used for on-premise network virtualization, as a peer to peer VPN
for mobile teams, for hybrid or multi-data-center cloud deployments, or just
about anywhere else secure software defined virtual networking is useful.

This is our OS-level client service. It allows Mac, Linux, Windows,
FreeBSD, and soon other types of clients to join BackOne virtual networks
like conventional VPNs or VLANs. It can run on native systems, VMs, or
containers (Docker, OpenVZ, etc.).

%prep
%if 0%{?rhel} >= 7
rm -rf *
ln -s %{getenv:PWD} %{name}-%{version}
tar --exclude=%{name}-%{version}/.git --exclude=%{name}-%{version}/%{name}-%{version} -czf %{_sourcedir}/%{name}-%{version}.tar.gz %{name}-%{version}/*
rm -f %{name}-%{version}
cp -a %{getenv:PWD}/* .
%endif

%build
#%if 0%{?rhel} <= 7
#make CFLAGS="`echo %{optflags} | sed s/stack-protector-strong/stack-protector/`" CXXFLAGS="`echo %{optflags} | sed s/stack-protector-strong/stack-protector/`" ZT_USE_MINIUPNPC=1 %{?_smp_mflags} one manpages selftest
#%else
%if 0%{?rhel} >= 7
make ZT_USE_MINIUPNPC=1 %{?_smp_mflags} one
%endif

%pre
%if 0%{?rhel} >= 7
/usr/bin/getent passwd backone || /usr/sbin/useradd -r -d /var/lib/backone -s /sbin/nologin backone
%endif
%if 0%{?fedora} >= 21
/usr/bin/getent passwd backone || /usr/sbin/useradd -r -d /var/lib/backone -s /sbin/nologin backone
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?rhel} < 7
pushd %{getenv:PWD}
%endif
make install DESTDIR=$RPM_BUILD_ROOT
%if 0%{?rhel} < 7
popd
%endif
%if 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp %{getenv:PWD}/debian/backone.service $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%endif
%if 0%{?fedora} >= 21
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp ${getenv:PWD}/debian/backone.service $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%endif
%if 0%{?rhel} <= 6
mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp %{getenv:PWD}/ext/installfiles/linux/backone.init.rhel6 $RPM_BUILD_ROOT/etc/init.d/backone
chmod 0755 $RPM_BUILD_ROOT/etc/init.d/backone
%endif

%files
%{_sbindir}/*
%{_mandir}/*
%{_localstatedir}/*
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%endif
%if 0%{?fedora} >= 21
%{_unitdir}/%{name}.service
%endif
%if 0%{?rhel} <= 6
/etc/init.d/backone
%endif

%post
%if 0%{?rhel} >= 7
%systemd_post backone.service
%endif
%if 0%{?fedora} >= 21
%systemd_post backone.service
%endif
%if 0%{?rhel} <= 6
case "$1" in
  1)
    chkconfig --add backone
  ;;
  2)
    chkconfig --del backone
    chkconfig --add backone
  ;;
esac
%endif

%preun
%if 0%{?rhel} >= 7
%systemd_preun backone.service
%endif
%if 0%{?fedora} >= 21
%systemd_preun backone.service
%endif
%if 0%{?rhel} <= 6
case "$1" in
  0)
    service backone stop
    chkconfig --del backone
  ;;
  1)
    # This is an upgrade.
    :
  ;;
esac
%endif

%postun
%if 0%{?rhel} >= 7
%systemd_postun_with_restart backone.service
%endif
%if 0%{?fedora} >= 21
%systemd_postun_with_restart backone.service
%endif

%changelog
