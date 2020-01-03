from flask import json, Response, request
from marshmallow import fields, Schema
from flask_restplus import fields as f

from app.utils.query import Query

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
            self.add_pagination(data)
        return Response(json.dumps(data), status=self.status, mimetype='application/json')

    def add_pagination(self, data):
        page = int(Query.get_param('page'))
        per_page = Query.get_param('per_page')
        if page > 1:
            data["prev"] = request.base_url + f'?page={page - 1}&per_page={per_page}'
        data["next"] = request.base_url + f'?page={page + 1}&per_page={per_page}'
        data["current"] = request.base_url + f'?page={page}&per_page={per_page}'
