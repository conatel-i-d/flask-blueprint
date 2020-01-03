import functools
from flask import request

from app.utils.query import Query

def parse_query_parameters(f):
  @functools.wraps(f)
  def decorated_function(*args, **kwargs):
    Query.parse_request(request)    
    return f(*args, **kwargs)
  return decorated_function
