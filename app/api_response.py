from flask import json, Response


class ApiResponse(object):
    def __init__(self, value, status=200):
        self.value = value
        self.status = status

    def to_response(self):
        if self.value == None:
            return Response('', status=self.status)
        data = {}
        if isinstance(self.value, dict):
            data['item'] = self.value
        if isinstance(self.value, list):
            data['items'] = self.value
            data['count'] = len(self.value)
        return Response(json.dumps(data), status=self.status, mimetype='application/json')