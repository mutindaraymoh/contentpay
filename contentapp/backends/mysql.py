"""
Custom MySQL backend wrapper for Django 6.0.2
"""
from django.db.backends.mysql import base

# Patch the MySQL constants
try:
    from MySQLdb.constants import ER
    
    # Add missing CONSTRAINT_FAILED constant if needed
    if not hasattr(ER, 'CONSTRAINT_FAILED'):
        ER.CONSTRAINT_FAILED = 4025
        print("Added missing CONSTRAINT_FAILED constant")
except ImportError:
    pass

# Re-export everything from the original backend
from django.db.backends.mysql.base import *  # noqa

# Ensure DatabaseWrapper is available
DatabaseWrapper = base.DatabaseWrapper