"""
WSGI config for contentpay project.
"""

import os

# Apply MySQL patches before any Django imports
try:
    import patch_mysql
    patch_mysql.apply_all_patches()
except ImportError:
    print("Warning: MySQL patch module not found")
except Exception as e:
    print(f"Warning: Failed to apply MySQL patches: {e}")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contentpay.settings')

application = get_wsgi_application()