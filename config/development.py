config = {
    'production': False,
    'development': True,

    'DB': {
        'name': 'foo',
        'host': 'localhost',
        'port': 27017
     },

    'gravatar': {
        'enabled': False
    },
}


def isEnabled(key):
     cfg = config.get(key, {})
     return cfg.get('enabled', False)
