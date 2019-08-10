from flask import Flask

from app.api_response import ApiResponse


class ApiFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, ApiResponse):
            return rv.to_response()
        return Flask.make_response(self, rv)