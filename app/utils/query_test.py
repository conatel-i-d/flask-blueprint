from flask import request, g
from app.test.fixtures import app
from app.utils.query import Query

def test_index_query_params(app):
    with app.app_context():
        expected = {
            'page': {
                'description': 'Requested items page. Defaults to 1.'
            }, 
            'per_page': {
                'description': 'Ammount of items per page. Defaults to 20.'
            },
            'order_by': {
                'description': 'Identifies the column in which to order the results.'
            },
            'order_dir': {
                'description': 'Selects the direction in which the results should be sorted. Only allows `asc` and `desc` as values.'
            }
        }
        assert Query.index_query_params == expected

def test_parse_request(app):
    with app.test_request_context('/healthz/?page=3&per_page=40&order_by=test&order_dir=up'):
        Query.parse_request(request)
        assert g.page == '3'
        assert g.per_page == '40'
        assert g.order_by == 'test'
        assert g.order_dir == 'up'

