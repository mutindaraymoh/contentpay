#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Apply MySQL patches before any Django imports
try:
    import patch_mysql
    patch_mysql.apply_all_patches()
except ImportError:
    print("Warning: MySQL patch module not found")
except Exception as e:
    print(f"Warning: Failed to apply MySQL patches: {e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contentpay.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()