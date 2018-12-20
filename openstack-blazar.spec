%global git_branch chameleoncloud-stable-rocky

Name:           openstack-blazar
Epoch:          1
Summary:        OpenStack Reservation (blazar)
Version:        2.0.0
Release:        11%{?dist}
License:        ASL 2.0
URL:            http://www.openstack.org

# Fetch the latest source from the chameleoncloud/stable/rocky branch
Source0:        https://github.com/ChameleonCloud/blazar/archive/chameleoncloud/stable/rocky/blazar-%{version}.tar.gz

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
install -p -D -m 644 blazar/db/migration/alembic.ini %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic.ini
install -p -D -d blazar/db/migration/alembic_migrations %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations
install -p -D -d blazar/db/migration/alembic_migrations/versions %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations/versions
install -p -D -m 644 blazar/db/migration/alembic_migrations/*.* %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations
install -p -D -m 644 blazar/db/migration/alembic_migrations/versions/*.* %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations/versions
install -p -D -m 644 blazar/db/migration/alembic_migrations/versions/README %{buildroot}/%{python_sitelib}/blazar/db/migration/alembic_migrations/versions/README

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
%{_bindir}/blazar-api-wsgi
%{_bindir}/blazar-db-manage
%{_bindir}/blazar-manager
%{_bindir}/blazar-rpc-zmq-receiver
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
* Thu Dec 20 2018 Cody Hammock <hammock@tacc.utexas.edu> 1:2.0.0-11
- Change permissions for db/migration directory.
* Tue Oct 30 2018 Pierre Riteau <pierre@stackhpc.com> 1:2.0.0-10
- openstack/blazar: a8dd03eb9de254544c217ac59b8acba0b023f29b
* Mon Oct 29 2018 Pierre Riteau <pierre@stackhpc.com> 1:2.0.0-9
- openstack/blazar: eec7c5fbd4c89a13035b93e3918856e98a100982
* Wed Oct 17 2018 Jason Anderson <jasonanderson@uchicago.edu> 1:2.0.0-8
- openstack/blazar: e67454d376d4cf20e999ab933e9bdb7eb7a30fc2
* Thu Sep 20 2018 Jason Anderson <jasonanderson@uchicago.edu> 1:2.0.0-7
- openstack/blazar: 23c23aeb904108497a35e21d13aa9b3945a88f2c
* Wed Sep 19 2018 Jacob Colleran <jakecoll@uchicago.edu> 1:2.0.0-6
- Updating with latest changes
* Tue Aug 28 2018 Pierre Riteau <pierre@stackhpc.com> 1:2.0.0-1
- Initial packaging for Rocky
