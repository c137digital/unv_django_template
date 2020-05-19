BASE_SETTINGS = {
    'app': {
        'components': []
    },
    'deploy': {
        'components': {
            'django': {
                'bin': 'uwsgi',
                'systemd': {
                    'instances': {'percent': 100}
                }
            },
            'redis': {
                'listen_private_ip': True
            },
            'nginx': {
                'geoip2': False
            }
        },
        'tasks': [
            # by default use all tasks from component only
            # if I need to add manually
            'unv.deploy.components.vagrant:VagrantTasks',
            'unv.deploy.components.nginx:NginxTasks',
            'unv.deploy.components.iptables:IPtablesTasks',
            'unv.deploy.components.redis:RedisTasks',
            'unv.deploy.components.postgres:PostgresTasks',

            'app.components.django.deploy:DjangoAppTasks'
        ],
    }
}
