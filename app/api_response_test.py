from flask import Response

from app.api_response import ApiResponse
from app.test.fixtures import app

def test_api_response_to_response_returns_a_response_object(app):
    with app.test_request_context('/healthz'):
        expected = ApiResponse(value=None).to_response()
        assert isinstance(expected, Response)

def test_api_response_to_response_empty_value_mimetype(app):
    with app.test_request_context('/healthz'):
        expected = ApiResponse(value=None).to_response()
        assert expected.mimetype == 'application/json'

def test_api_response_to_response_default_status(app):
    with app.test_request_context('/healthz'):    
        expected = ApiResponse(value=None).to_response()
        assert expected.status == '200 OK'

def test_api_response_to_response_value_mimetype(app):
    with app.test_request_context('/healthz'):    
        expected = ApiResponse(value={'ok': True}).to_response()
        assert expected.mimetype == 'application/json'

def test_api_response_to_response_empty_body(app):
    with app.test_request_context('/healthz'): 
        expected = ApiResponse(value=None).to_response()
        assert expected.data == b''

def test_api_response_to_response_single_value_body(app):
    with app.test_request_context('/healthz'):    
        expected = ApiResponse(value={'ok': True}).to_response()
        assert expected.data == b'{"item": {"ok": true}}'

def test_api_response_to_response_multiple_value_body(app):
    with app.test_request_context('/healthz'):
        expected = ApiResponse(value=[{'ok': True}, {'ok': False}]).to_response()
        assert expected.data == b'{"count": 2, "current": "http://localhost/healthz?page=1&per_page=3", "items": [{"ok": true}, {"ok": false}], "next": "http://localhost/healthz?page=2&per_page=3"}'



