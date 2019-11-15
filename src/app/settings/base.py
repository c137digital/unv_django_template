BASE_SETTINGS = {
    'app': {
        'components': [
            'app.components.site',
        ]
    },
    'deploy': {
        'components': {
            'django': {
                'bin': 'uwsgi',
                'use_https': False,
                'systemd': {
                    'instances': {'percent': 100}
                }
            },
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
