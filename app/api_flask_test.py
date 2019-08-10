from flask import Response

from app.api_flask import ApiFlask
from app.api_response import ApiResponse
from app.test.fixtures import app


def test_api_flask_make_response(app):
    #should convert the ApiResponse object to a `Response` by calling its `to_response` method.
    api_response = ApiResponse(value={'ok': True}, status=200)
    response = app.make_response(api_response)
    expected = isinstance(response, Response)
    assert expected == True
    assert response.mimetype == 'application/json'
    assert response.status == '200 OK'
    assert response.data == b'{"ok": true}'