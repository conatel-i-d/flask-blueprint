from flask import json, Response
from marshmallow import fields, Schema
from flask_restplus import fields as f


class ApiResponse(object):
    def __init__(self, value, status=200):
        self.value = value
        self.status = status

    def to_response(self):
        if self.value == None:
            return Response('', status=self.status, mimetype='application/json')
        if self.status == 400:
            return Response(json.dumps(self.value), status=self.status,
                    mimetype='application/json')
        data = {}
        if isinstance(self.value, dict):
            data['item'] = self.value
        if isinstance(self.value, list):
            data['items'] = self.value
            data['count'] = len(self.value)
        return Response(json.dumps(data), status=self.status, mimetype='application/json')
