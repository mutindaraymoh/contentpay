from django.apps import AppConfig

class ContentappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contentapp'
    
    def ready(self):
        """Apply MySQL patches when the app is ready"""
        import os
        if os.environ.get('RUN_MAIN') == 'true':  # Only run once in development
            try:
                from MySQLdb.constants import ER
                if not hasattr(ER, 'CONSTRAINT_FAILED'):
                    ER.CONSTRAINT_FAILED = 4025
                    print("✓ Applied MySQL patch: added CONSTRAINT_FAILED")
            except ImportError:
                pass