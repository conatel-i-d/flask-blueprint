from flask import g, current_app

class Query:
    index_query_params = dict(    
        page="Requested items page. Defaults to 1.",
        per_page="Ammount of items per page. Defaults to 20."
    ) 

    @staticmethod
    def get_param(name):
        return g.get(name, current_app.config[name.upper()])

    @staticmethod
    def parse_request(request):
        g.page = request.args.get('page', current_app.config['PAGE'])
        g.per_page = request.args.get('per_page', current_app.config['PER_PAGE'])

