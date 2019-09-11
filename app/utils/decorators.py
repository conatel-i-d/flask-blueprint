import functools

from flask import g, request

LIMIT = 10
OFFSET = 0

def parse_query_parameters(f):
  @functools.wraps(f)
  def decorated_function(*args, **kwargs):
    # Do something with your request here
    g.limit = request.args.get('limit', LIMIT)
    g.offset = request.args.get('offset', OFFSET)
    return f(*args, **kwargs)
  return decorated_function