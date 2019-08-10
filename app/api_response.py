from flask import json, Response


class ApiResponse(object):
    def __init__(self, value, status=200):
        self.value = value
        self.status = status

    def to_response(self):
        return Response(json.dumps(self.value), status=self.status, mimetype='application/json')