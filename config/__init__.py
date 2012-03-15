import os

if os.environ.get('QR_ENVIRONMENT') == "PRODUCTION":
    from production import *
else:
    from development import *
