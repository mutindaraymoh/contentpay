# contentapp/backends/mysql_retry.py
import time
import logging
from django.db.backends.mysql import base

logger = logging.getLogger(__name__)

class DatabaseWrapper(base.DatabaseWrapper):
    """MySQL database backend with automatic retry on connection failure"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def get_new_connection(self, conn_params):
        """Get new connection with retry logic"""
        for attempt in range(self.max_retries):
            try:
                return super().get_new_connection(conn_params)
            except Exception as e:
                if 'Lost connection' in str(e) or 'timeout' in str(e).lower():
                    if attempt < self.max_retries - 1:
                        logger.warning(f"Connection attempt {attempt + 1} failed: {e}. Retrying...")
                        time.sleep(self.retry_delay * (attempt + 1))
                    else:
                        logger.error(f"All connection attempts failed: {e}")
                        raise
                else:
                    # If it's not a connection error, raise immediately
                    raise
    
    def create_cursor(self, name=None):
        """Create cursor with retry logic for lost connections"""
        for attempt in range(self.max_retries):
            try:
                return super().create_cursor(name)
            except Exception as e:
                if 'Lost connection' in str(e) or 'MySQL server has gone away' in str(e):
                    if attempt < self.max_retries - 1:
                        logger.warning(f"Cursor creation failed, reconnecting... (attempt {attempt + 2})")
                        self.close()
                        self.connect()
                    else:
                        raise
                else:
                    raise
    
    def _set_autocommit(self, autocommit):
        """Handle autocommit with connection loss recovery"""
        for attempt in range(self.max_retries):
            try:
                return super()._set_autocommit(autocommit)
            except Exception as e:
                if 'Lost connection' in str(e) and attempt < self.max_retries - 1:
                    logger.warning(f"Connection lost during autocommit, reconnecting...")
                    time.sleep(self.retry_delay)
                    self.close()
                    self.connect()
                else:
                    raise

# Make sure to expose the same classes as the original backend
from django.db.backends.mysql.base import *  # noqa
from django.db.backends.mysql.base import __all__  # noqa

# Replace the DatabaseWrapper with our custom one
base.DatabaseWrapper = DatabaseWrapper