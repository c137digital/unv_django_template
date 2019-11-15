from unv.app.settings import ComponentSettings

from .base import BASE_SETTINGS

# NOTE: add check you don't import nothing with settings inside

SETTINGS = ComponentSettings.create({
    'app': {
        'env': 'dev'
    },
    'deploy': {
        'hosts': {
            'vagrant': {
                'public_ip': '10.60.25.10',
                'private_ip': '10.60.25.10',
                'components': ['iptables', 'nginx', 'django', 'postgres'],
            }
        },
        'components': {
            'django': {
                'settings': 'app.settings.dev',
            },
            'nginx': {
                'geoip2': True
            }
        }
    }
}, BASE_SETTINGS)
