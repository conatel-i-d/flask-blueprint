from flask import Response

from app.api_response import ApiResponse


def test_api_response_to_response_returns_a_response_object():
    api_response = ApiResponse(value={'ok': True}, status=200)
    expected = api_response.to_response()
    assert isinstance(expected, Response)