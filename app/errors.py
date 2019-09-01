from werkzeug.exceptions import HTTPException

from app.api_response import ApiResponse

class ApiException(HTTPException):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

    def to_response(self):
        return ApiResponse({'message': self.message}, status=self.code)

def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_response())