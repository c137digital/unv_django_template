from pathlib import Path

from unv.utils.collections import update_dict_recur
from unv.deploy.tasks import register, onehost, nohost
from unv.deploy.settings import SETTINGS as DEPLOY_SETTINGS
from unv.deploy.components.app import AppSettings, AppTasks


class DjangoAppSettings(AppSettings):
    NAME = 'django'
    SCHEMA = update_dict_recur(AppSettings.SCHEMA, {
        'host': {'type': 'string', 'required': True},
        'port': {'type': 'integer', 'required': True},
        'domain': {'type': 'string', 'required': True},
        'use_https': {'type': 'boolean', 'required': True},
        'ssl_certificate': {'type': 'string', 'required': True},
        'ssl_certificate_key': {'type': 'string', 'required': True},
        'nginx': {
            'type': 'dict',
            'schema': {
                'template': {'type': 'string', 'required': True},
                'name': {'type': 'string', 'required': True},
                'upstream_name': {'type': 'string', 'required': True}
            },
            'required': True
        },
        'iptables': {
            'type': 'dict',
            'schema': {
                'v4': {'type': 'string', 'required': True}
            },
            'required': True
        },
        'static': {
            'type': 'dict',
            'schema': {
                'link': {'type': 'boolean', 'required': True},
                'url': {'type': 'string', 'required': True},
                'dir': {'type': 'string', 'required': True}
            },
            'required': True
        }
    }, copy=True)

    DEFAULT = update_dict_recur(AppSettings.DEFAULT, {
        'host': '0.0.0.0',
        'port': 8000,
        'domain': 'app.local',
        'use_https': True,
        'ssl_certificate': 'secure/certs/fullchain.pem',
        'ssl_certificate_key': 'secure/certs/privkey.pem',
        'nginx': {
            'template': 'nginx.conf',
            'name': 'django.conf',
            'upstream_name': 'django'
        },
        'iptables': {
            'v4': 'ipv4.rules'
        },
        'static': {
            'link': True,
            'url': '/static',
            'dir': 'static'
        }
    }, copy=True)

    @property
    def ssl_certificate(self):
        return self.home_abs / self._data['ssl_certificate']

    @property
    def ssl_certificate_key(self):
        return self.home_abs / self._data['ssl_certificate_key']

    @property
    def host(self):
        return self._data['host']

    @property
    def port(self):
        return self._data['port']

    @property
    def nginx_config(self):
        nginx = self._data['nginx']
        template, path = nginx['template'], nginx['name']
        if not template.startswith('/'):
            template = (self.local_root / template).resolve()
        return Path(template), path

    @property
    def nginx_upstream_name(self):
        return self._data['nginx']['upstream_name']

    @property
    def domain(self):
        return self._data['domain'].encode('idna').decode()

    @property
    def server_domains(self):
        """Return utf-8 domain and encoded by idna."""
        domains = [self.domain]
        if self._data['domain'] != self.domain:
            domains.append(self._data['domain'])
        return ' '.join(domains)

    @property
    def static_link(self):
        return self._data['static']['link']

    @property
    def static_dir(self):
        return self.home_abs / Path(self._data['static']['dir'])

    @property
    def static_url(self):
        return self._data['static']['url']

    @property
    def use_https(self):
        return self._data['use_https']

    @property
    def iptables_v4_rules(self):
        return (self.local_root / self._data['iptables']['v4']).read_text()


SETTINGS = DjangoAppSettings()


class DjangoAppTasks(AppTasks):
    SETTINGS = SETTINGS

    async def get_iptables_template(self):
        return self.settings.iptables_v4_rules

    async def get_nginx_include_configs(self):
        return [self.settings.nginx_config]

    async def get_upstream_servers(self):
        for _, host in DEPLOY_SETTINGS.get_hosts(self.settings.NAME):
            with self._set_host(host):
                settings = self.settings.systemd['instances']
                count = await self._calc_instances_count(**settings)
            for instance in range(1, count + 1):
                yield f"{host['private_ip']}:{self.settings.port + instance}"

    @register
    @onehost
    async def shell(self):
        return await self._python.run(
            'manage shell', interactive=True,
            prefix=f'SETTINGS={self.settings.module}'
        )

    @register
    async def sync(self, type_=''):
        await super().sync(type_)

        # TODO: we need this stuff to deliver remotly because of db on other server
        # TODO: fix user paths
        # TODO: fix PATH escape symbols
        # TODO: move to setup
        with self._prefix(r'PATH=\$PATH:/home/postgres/app/bin'):
            await self._run('/home/django/python/bin/pip install psycopg2')

        await self._sudo('ldconfig /home/postgres/app/lib')

        await self.manage('collectstatic --noinput')

    @register
    @onehost
    async def manage(self, command):
        print(await self._python.run(
            f'manage {command}',
            prefix=f'PYTHONPATH=/home/django/ SETTINGS={self.settings.module}',
            interactive=True
        ))

    @register
    async def upload_static(self):
        await self._sudo('chown -hR django /home/django/m')
        await self._rsync('../m.bgram.app/dist', '/home/django/m')
        await self._sudo('chown -hR nginx /home/django/m')

    @register
    async def update_hosts(self):
        await self._local(
            f'sudo bash -c \'echo "{self.public_ip} {self.settings.domain}"'
            ' >> /etc/hosts\'')

    @register
    @nohost
    async def reinit(self):
        import os
        # FIXME: why settings in env
        # print(os.environ)
        os.environ.pop('SETTINGS')
        os.system(
            "deploy dev postgres.restart")
        os.system(
            "deploy dev postgres.drop_database:django_db")
        os.system(
            "deploy dev postgres.create_user:django_user")
        os.system(
            'deploy dev postgres.create_database:django_db,django_user')
        os.system('rm -f src/app/components/someapp/migrations/*.py')
        os.system(
            'touch src/app/components/someapp/migrations/__init__.py')
        os.system('manage makemigrations')
        os.system(
            'deploy dev django.sync django.manage:makemigrations '
            'django.manage:migrate'
        )
