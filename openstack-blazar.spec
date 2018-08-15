%global git_branch chameleoncloud-ocata

Name:           openstack-blazar
Epoch:          1
Summary:        OpenStack Reservation (blazar)
Version:        0.3.0
Release:        9%{?dist}
License:        ASL 2.0
URL:            http://www.openstack.org

# Fetch the latest source from the chameleoncloud/ocata branch
Source0:        https://github.com/ChameleonCloud/blazar/archive/chameleoncloud/ocata/blazar-%{version}.tar.gz

Source1:        openstack-blazar-api.service
Source2:        openstack-blazar-manager.service
Source3:        blazar.logrotate
Source4:        blazar.conf.sample

BuildArch:        noarch
BuildRequires:    openstack-macros
BuildRequires:    python-pbr
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    systemd-units

Requires:         python-alembic
Requires:         python-babel
Requires:         python-eventlet
Requires:         python-flask
Requires:         python-iso8601
Requires:         python-keystoneclient
Requires:         python-keystonemiddleware
Requires:         python-kombu
Requires:         python-migrate
Requires:         python-netaddr
Requires:         python-novaclient
Requires:         python-oslo-concurrency
Requires:         python-oslo-config
Requires:         python-oslo-db
Requires:         python-oslo-i18n
Requires:         python-oslo-log
Requires:         python-oslo-messaging
Requires:         python-oslo-middleware
Requires:         python-oslo-policy
Requires:         python-oslo-serialization
Requires:         python-oslo-service
Requires:         python-oslo-utils
Requires:         python-pbr
Requires:         python-pecan
Requires:         python-posix_ipc
Requires:         python-redis
Requires:         python-routes
Requires:         python-sqlalchemy
Requires:         python-stevedore
Requires:         python-webob
Requires:         python-wsme

%prep
%setup -q -n blazar-%{git_branch}
rm requirements.txt test-requirements.txt

%build
PBR_VERSION=%{version} %{__python2} setup.py build

%install
PBR_VERSION=%{version} %{__python2} setup.py install --skip-build --root=%{buildroot}

install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-blazar

# Install systemd scripts
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_sharedstatedir}/blazar/
mkdir -p %{buildroot}%{_localstatedir}/log/blazar/

# Populate the conf dir
install -p -D -m 640 %{SOURCE4} %{buildroot}/%{_sysconfdir}/blazar/blazar.conf
install -p -D -m 640 etc/policy.json %{buildroot}/%{_sysconfdir}/blazar/policy.json

# Copy DB migration config
install -p -D -m 640 blazar/db/migration/alembic.ini %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic.ini
install -p -D -d blazar/db/migration/alembic_migrations %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations
install -p -D -d blazar/db/migration/alembic_migrations/versions %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations/versions
install -p -D -m 640 blazar/db/migration/alembic_migrations/*.* %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations
install -p -D -m 640 blazar/db/migration/alembic_migrations/versions/*.* %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations/versions
install -p -D -m 640 blazar/db/migration/alembic_migrations/versions/README %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations/versions/README

%pre
getent group blazar >/dev/null || groupadd -r blazar
getent passwd blazar >/dev/null || \
    useradd -r -g blazar -d %{_sharedstatedir}/blazar -s /sbin/nologin \
-c "OpenStack Blazar Daemons" blazar
exit 0

%description
OpenStack Reservation-as-a-Service (codename Blazar) is open source software
aiming to allow the reservation of both virtual and physical resources in a
calendar based on various reservation criteria.

This package contains the Blazar daemon services.

%files
%{_bindir}/blazar-api
%{_bindir}/blazar-db-manage
%{_bindir}/blazar-manager
%{_bindir}/blazar-rpc-zmq-receiver
%{_bindir}/climate-api
%{_bindir}/climate-db-manage
%{_bindir}/climate-manager
%{_bindir}/climate-rpc-zmq-receiver
%doc LICENSE
%doc README.rst
%{_unitdir}/openstack-blazar-api.service
%{_unitdir}/openstack-blazar-manager.service
%dir %attr(0750, root, blazar) %{_sysconfdir}/blazar
%config(noreplace) %attr(0640, root, blazar) %{_sysconfdir}/blazar/blazar.conf
%config(noreplace) %attr(0640, blazar, blazar) %{_sysconfdir}/blazar/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-blazar
%dir %attr(-, blazar, blazar) %{_sharedstatedir}/blazar
%dir %attr(0750, blazar, blazar) %{_localstatedir}/log/blazar
%{python_sitelib}/blazar
%{python_sitelib}/blazar-%{version}-*.egg-info

%changelog
* Wed Aug 23 2017 Pierre Riteau <priteau@uchicago.edu> 1:0.3.0-1
- Initial packaging for Ocata
