import functools
from flask import g, request, current_app

from app.config import get_config

def parse_query_parameters(f):
  @functools.wraps(f)
  def decorated_function(*args, **kwargs):
    g.page = request.args.get('page', current_app.config['PAGE'])
    g.per_page = request.args.get('per_page', current_app.config['PER_PAGE'])
    return f(*args, **kwargs)
  return decorated_function
