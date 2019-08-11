from flask_restplus import Api

from app.api_response import ApiResponse


class ApiFlask(Api):
    def make_response(self, rv, *args, **kwargs):
        if isinstance(rv, ApiResponse):
            return rv.to_response()
        return Api.make_response(self, rv, *args, **kwargs)