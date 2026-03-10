import os
import django
import MySQLdb

# MySQLdb doesn't have __version__, so we'll check differently
print("MySQLdb imported successfully")
print(f"MySQLdb location: {MySQLdb.__file__}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contentpay.settings')
django.setup()

from django.db import connection

print("\nTesting MySQL connection...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✓ Connected successfully!")
        print(f"MySQL Version: {version[0]}")
        print(f"Database: {connection.settings_dict['NAME']}")
        print(f"Host: {connection.settings_dict['HOST']}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    import traceback
    traceback.print_exc()