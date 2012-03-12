import os

if os.environ.get('QR_ENVIRONMENT') == "PRODUCTION":
    from production import config
else:
    from development import config
