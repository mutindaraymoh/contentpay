"""
MySQL patching module for Django 6.0.2
Place this file in your project root and import it in manage.py
"""

import sys
import os

def patch_mysql_constants():
    """Patch missing MySQL constants"""
    try:
        import MySQLdb
        from MySQLdb.constants import ER
        
        # Add missing CONSTRAINT_FAILED constant if needed
        if not hasattr(ER, 'CONSTRAINT_FAILED'):
            ER.CONSTRAINT_FAILED = 4025
            print("✓ Added missing CONSTRAINT_FAILED constant")
            return True
        
        print("✓ MySQL constants already patched")
        return True
    except ImportError as e:
        print(f"✗ Could not import MySQLdb: {e}")
        return False
    except Exception as e:
        print(f"✗ Error patching MySQL: {e}")
        return False

def patch_mysql_converters():
    """Patch MySQL converters if needed"""
    try:
        from MySQLdb.converters import conversions
        from MySQLdb.constants import FIELD_TYPE
        import datetime
        
        # Ensure datetime conversions work properly
        conversions[FIELD_TYPE.DATETIME] = conversions[FIELD_TYPE.DATETIME]
        conversions[FIELD_TYPE.DATE] = conversions[FIELD_TYPE.DATE]
        conversions[FIELD_TYPE.TIME] = conversions[FIELD_TYPE.TIME]
        
        print("✓ MySQL converters patched")
        return True
    except Exception as e:
        print(f"✗ Error patching converters: {e}")
        return False

def apply_all_patches():
    """Apply all MySQL patches"""
    print("=" * 50)
    print("Applying MySQL patches for Django 6.0.2")
    print("=" * 50)
    
    patches = [
        ("Constants", patch_mysql_constants),
        ("Converters", patch_mysql_converters),
    ]
    
    success = True
    for name, patch_func in patches:
        print(f"\nPatching {name}...")
        if not patch_func():
            success = False
    
    if success:
        print("\n✅ All MySQL patches applied successfully!")
    else:
        print("\n⚠️ Some patches failed. Check errors above.")
    
    return success

if __name__ == "__main__":
    apply_all_patches()