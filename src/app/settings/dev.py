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
                'public_ip': '10.50.40.15',
                'private_ip': '0.0.0.0',
                'components': [
                    'iptables', 'nginx', 'django', 'postgres', 'redis'
                ],
            }
        },
        'components': {
            'django': {
                'settings': 'app.settings.dev',
                'domain': 'app.local',
                'use_https': False
            },
            'nginx': {
                'geoip2': False
            }
        }
    }
}, BASE_SETTINGS)
