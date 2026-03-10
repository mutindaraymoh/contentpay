import os
import django

def patch_mysql_backend():
    """Patch the MySQL backend to work with Django 6.0.2"""
    try:
        # Find the MySQL backend directory
        import MySQLdb
        import pkgutil
        
        # This is the file we need to patch
        import django.db.backends.mysql.base
        
        # Add the missing CONSTANT_FAILED attribute if it doesn't exist
        from MySQLdb.constants import ER
        
        if not hasattr(ER, 'CONSTRAINT_FAILED'):
            # Add the missing constant
            ER.CONSTRAINT_FAILED = 4025  # Typical value for this error
            print("✓ Added missing CONSTRAINT_FAILED constant")
        
        print("✓ MySQL backend patched successfully")
    except Exception as e:
        print(f"✗ Failed to patch MySQL backend: {e}")

if __name__ == "__main__":
    patch_mysql_backend()