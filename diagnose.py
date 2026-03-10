import os
import sys

print("=" * 50)
print("DIAGNOSIS TOOL")
print("=" * 50)

print(f"\nCurrent directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

print("\n" + "=" * 50)
print("CHECKING FILES AND FOLDERS")
print("=" * 50)

# Check contentapp folder
if os.path.exists('contentapp'):
    print("\n✓ contentapp folder exists")
    print("\nFiles in contentapp:")
    for file in os.listdir('contentapp'):
        print(f"  - {file}")
else:
    print("\n✗ contentapp folder NOT found")

# Check contentpay folder
if os.path.exists('contentpay'):
    print("\n✓ contentpay folder exists")
    print("\nFiles in contentpay:")
    for file in os.listdir('contentpay'):
        if file.endswith('.py'):
            print(f"  - {file}")
else:
    print("\n✗ contentpay folder NOT found")

# Check manage.py
if os.path.exists('manage.py'):
    print("\n✓ manage.py exists")
else:
    print("\n✗ manage.py NOT found")

print("\n" + "=" * 50)
print("RECOMMENDED ACTIONS")
print("=" * 50)
print("\n1. Make sure contentapp/urls.py exists")
print("2. Make sure contentapp/views.py exists")
print("3. Check INSTALLED_APPS in settings.py")
print("4. Run: python manage.py check")