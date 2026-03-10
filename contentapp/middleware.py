# contentapp/middleware.py
from django.db import connection

class MySQLConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check if the connection is usable
        if connection.connection and not connection.is_usable():
            connection.close()

        response = self.get_response(request)

        # Do NOT close every time — let Django reuse connections
        return response