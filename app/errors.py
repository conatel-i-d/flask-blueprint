from werkzeug.exceptions import HTTPException

from app.api_response import ApiResponse

class ApiException(HTTPException):
    def __init__(self, message, status=400, code='UncaughtError'):
        self.message = message
        self.status = status
        self.code = code

    def to_response(self):
        response = dict(message=self.message, code=self.code)
        return ApiResponse(response, status=self.status).to_response()

def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_response())

# Aca se deben incluir tipos de error específicos de la aplicación
