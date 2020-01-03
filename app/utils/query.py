from flask import g, current_app

class Query:
    index_query_params = {
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

    @staticmethod
    def get_param(name):
        return g.get(name, current_app.config.get(name.upper(), None))

    @staticmethod
    def parse_request(request):
        g.page = request.args.get('page', current_app.config['PAGE'])
        g.per_page = request.args.get('per_page', current_app.config['PER_PAGE'])
        g.order_by = request.args.get('order_by', None)
        g.order_dir = request.args.get('order_dir', None)

