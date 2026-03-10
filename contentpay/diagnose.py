import os
import sys

print("=" * 50)
print("DIAGNOSIS TOOL")
print("=" * 50)

# Check current directory
print(f"\nCurrent directory: {os.getcwd()}")

# Check if manage.py exists
if os.path.exists('manage.py'):
    print("✓ manage.py found")
else:
    print("✗ manage.py NOT found")

# Check contentapp folder
if os.path.exists('contentapp'):
    print("✓ contentapp folder found")
    
    # Check contentapp files
    required_files = ['__init__.py', 'views.py', 'urls.py', 'apps.py']
    for file in required_files:
        if os.path.exists(f'contentapp/{file}'):
            print(f"  ✓ contentapp/{file} found")
        else:
            print(f"  ✗ contentapp/{file} NOT found")
else:
    print("✗ contentapp folder NOT found")

# Check contentpay folder
if os.path.exists('contentpay'):
    print("\n✓ contentpay folder found")
    
    # Check contentpay files
    if os.path.exists('contentpay/__init__.py'):
        print("  ✓ contentpay/__init__.py found")
    else:
        print("  ✗ contentpay/__init__.py NOT found")
    
    if os.path.exists('contentpay/settings.py'):
        print("  ✓ contentpay/settings.py found")
    else:
        print("  ✗ contentpay/settings.py NOT found")
    
    if os.path.exists('contentpay/urls.py'):
        print("  ✓ contentpay/urls.py found")
    else:
        print("  ✗ contentpay/urls.py NOT found")
else:
    print("✗ contentpay folder NOT found")

print("\n" + "=" * 50)
print("PYTHON PATH:")
for p in sys.path:
    print(f"  {p}")
print("=" * 50)

print("\nTry running these commands:")
print("1. python manage.py makemigrations")
print("2. python manage.py migrate")
print("3. python manage.py runserver")