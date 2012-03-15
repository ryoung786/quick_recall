config = {
    'production': True,
    'development': False,

    'DB': {
        'name': 'foo',
        'host': 'localhost',
        'port': 27017
     },

    'gravatar': {
        'enabled': True
    },
}


def isEnabled(key):
     cfg = config.get(key, {})
     return cfg.get('enabled', False)
