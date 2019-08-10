from werkzeug.exceptions import HTTPException

from app.api_response import ApiResponse

class ApiException(HTTPException):
    def __init__(self, description, code=400):
        self.description = description
        self.code = code

    def to_response(self):
        return ApiResponse({'description': self.description}, status=self.code)

def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_response())