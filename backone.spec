Name:           backone
Version:        1.10.3
Release:        1%{?dist}
Summary:        BackOne global ethernet swicth

License:        BackOne BSL 1.1
URL:            https://backone.cloud

# Fedora

%if "%{?dist}" == ".fc35"
BuildRequires: systemd clang openssl openssl-devel
Requires:      systemd openssl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%if "%{?dist}" == ".fc36"
BuildRequires: systemd clang openssl1.1 openssl1.1-devel
Requires:      systemd openssl1.1
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%if "%{?dist}" == ".fc37"
BuildRequires: systemd clang openssl1.1 openssl1.1-devel
Requires:      systemd openssl1.1
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

# RHEL

%if "%{?dist}" == ".el6"
Requires: chkconfig
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%if "%{?dist}" == ".el7"
BuildRequires: systemd openssl-devel
Requires:      systemd openssl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%if "%{?dist}" == ".el8"
BuildRequires: systemd openssl-devel
Requires:      systemd openssl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%if "%{?dist}" == ".el9"
BuildRequires: systemd openssl-devel
Requires:      systemd openssl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

# Amazon

%if "%{?dist}" == ".amzn2"
BuildRequires:  systemd openssl-devel
Requires:       systemd openssl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%if "%{?dist}" == ".amzn2022"
BuildRequires:  systemd openssl-devel
Requires:       systemd openssl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
%endif

%description
BackOne is a software defined networking layer for Earth.

It can be used for on-premise network virtualization, as a peer to peer VPN
for mobile teams, for hybrid or multi-data-center cloud deployments, or just
about anywhere else secure software defined virtual networking is useful.

This is our OS-level client service. It allows Mac, Linux, Windows,
FreeBSD, and soon other types of clients to join ZeroTier virtual networks
like conventional VPNs or VLANs. It can run on native systems, VMs, or
containers (Docker, OpenVZ, etc.).

%prep
%if "%{?dist}" != ".el6"
rm -rf BUILD BUILDROOT RPMS SRPMS SOURCES
ln -s %{getenv:PWD} %{name}-%{version}
mkdir -p SOURCES
tar --exclude=%{name}-%{version}/.git --exclude=%{name}-%{version}/%{name}-%{version} -czf SOURCES/%{name}-%{version}.tar.gz %{name}-%{version}/*
rm -f %{name}-%{version}
cp -a %{getenv:PWD}/* .
%endif

%build
%if "%{?dist}" != ".el6"
make ZT_USE_MINIUPNPC=1 %{?_smp_mflags} one
%endif

%pre
/usr/bin/getent passwd backone || /usr/sbin/useradd -r -d /var/lib/backone -s /sbin/nologin backone

%install
%if "%{?dist}" != ".el6"
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp %{getenv:PWD}/debian/backone.service $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%else
rm -rf $RPM_BUILD_ROOT
pushd %{getenv:PWD}
make install DESTDIR=$RPM_BUILD_ROOT
popd
mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp %{getenv:PWD}/ext/installfiles/linux/backone.init.rhel6 $RPM_BUILD_ROOT/etc/init.d/backone
chmod 0755 $RPM_BUILD_ROOT/etc/init.d/backone
%endif

%files
%{_sbindir}/*
%{_mandir}/*
%{_localstatedir}/*

%if 0%{?rhel} && 0%{?rhel} <= 6
/etc/init.d/backone
%else
%{_unitdir}/%{name}.service
%endif

%post
%if ! 0%{?rhel} && 0%{?rhel} <= 6
%systemd_post backone.service
%endif

%preun
%if ! 0%{?rhel} && 0%{?rhel} <= 6
%systemd_preun backone.service
%endif

%postun
%if ! 0%{?rhel} && 0%{?rhel} <= 6
%systemd_postun_with_restart backone.service
%endif

%changelog
