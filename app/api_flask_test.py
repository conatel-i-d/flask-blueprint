from flask import Response

from app.api_flask import ApiFlask
from app.api_response import ApiResponse
from app.test.fixtures import api


def test_api_flask_make_response(api):
    #should convert the ApiResponse object to a `Response` by calling its `to_response` method.
    api_response = ApiResponse(value={'ok': True}, status=200)
    response = api.make_response(api_response)
    expected = isinstance(response, Response)
    assert expected == True